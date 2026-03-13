import math
from sequence import BLINK_SEQUENCES

MATCH_THRESHOLD = 0.5


def extract_one_cycle(seq: list[float]) -> list[float]:
    """Return the first complete blink cycle from a sequence.

    A cycle ends at the first off-time (odd index) that exceeds 2x the median
    on-time. If no such gap exists (e.g. all intervals equal) the full sequence
    is returned unchanged, which is correct for Init/Precharge/Permanent-Fault.
    """
    if len(seq) < 2:
        return seq
    on_times = sorted(seq[0::2])
    n = len(on_times)
    median_on = (on_times[(n - 1) // 2] + on_times[n // 2]) / 2
    threshold = median_on * 2.0
    for i in range(1, len(seq), 2):
        if seq[i] > threshold:
            return seq[: i + 1]
    return seq


def normalize(seq: list[float]) -> list[float]:
    """Divide each element by total duration so scale differences don't affect matching."""
    total = sum(seq)
    return [x / total for x in seq] if total > 0 else seq


def dtw_distance(a: list[float], b: list[float]) -> float:
    """Dynamic Time Warping distance between two sequences.

    Robust to length mismatches and timing drift — allows stretching/compressing
    either sequence to find the best alignment.
    """
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    if n == 0 or m == 0:
        return math.inf

    dp = [[math.inf] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = (a[i - 1] - b[j - 1]) ** 2
            dp[i][j] = cost + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return math.sqrt(dp[n][m])


def _score_channel(detected: list[float], known: list[float]) -> float:
    """Return DTW distance between two normalized single-cycle sequences.

    Extracts one representative cycle from both sequences before comparing so
    the result is independent of how many cycles the video happened to capture.
    Returns inf if either sequence is empty.
    """
    if not detected or not known:
        return math.inf
    nd = normalize(extract_one_cycle(detected))
    nk = normalize(extract_one_cycle(known))
    return dtw_distance(nd, nk)


def match_sequence(
    r_times: list[float],
    g_times: list[float],
    b_times: list[float],
    threshold: float = MATCH_THRESHOLD,
) -> tuple[str, float]:
    """Match detected per-channel time sequences against all known BLINK_SEQUENCES.

    For each known state, scores are computed only on channels that are active
    (non-empty) in the reference. Channels where both detected and reference are
    empty are ignored. The per-channel scores are averaged to produce a final score.

    Returns:
        (state_name, score) — state_name is "Unknown" when score > threshold.
    """
    detected = {"R": r_times, "G": g_times, "B": b_times}

    best_name = "Unknown"
    best_score = math.inf

    for name, channels in BLINK_SEQUENCES.items():
        active_colors = [c for c in ("R", "G", "B") if channels.get(c)]

        if not active_colors:
            continue

        channel_scores = []
        for color in active_colors:
            score = _score_channel(detected[color], channels[color])
            channel_scores.append(score)

        combined = sum(channel_scores) / len(channel_scores)

        if combined < best_score:
            best_score = combined
            best_name = name

    if best_score > threshold:
        return "Unknown", best_score

    return best_name, best_score
