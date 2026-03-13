import numpy as np
import cv2
from itertools import dropwhile
from sequence_matcher import match_sequence


def remove_leading_zeros(sequence: list):
    return list(dropwhile(lambda x: x == 0, sequence))


def remove_short_on_runs(sequence: list, min_run: int = 4) -> list:
    """Zero out any contiguous run of 1s shorter than min_run frames.

    At ~26 fps a run of 4 frames = ~154 ms, which is the practical minimum
    detectable pulse for the states of interest. Shorter runs are noise.
    """
    seq = sequence[:]
    i = 0
    while i < len(seq):
        if seq[i] == 1:
            j = i
            while j < len(seq) and seq[j] == 1:
                j += 1
            if j - i < min_run:
                for k in range(i, j):
                    seq[k] = 0
            i = j
        else:
            i += 1
    return seq


def largest_cluster_area(mask) -> float:
    """Return the area of the largest single connected component in a binary mask."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0.0
    return max(cv2.contourArea(c) for c in contours)


def build_time_sequence(sequence: list, fps: float) -> tuple[list[list[int]], list[float]]:
    """Segment a binary sequence into runs and convert each run to a duration in seconds."""
    if not sequence:
        return [], []
    list_result = [[]]
    for i in range(len(sequence)):
        if i > 0 and sequence[i] != sequence[i - 1]:
            list_result.append([])
        list_result[-1].append(sequence[i])
    time_sequence = [len(run) / fps for run in list_result]
    return list_result, time_sequence


def flip_correct(sequence: list) -> list:
    """Correct single isolated bit flips (one-off noise)."""
    seq = sequence[:]
    for i in range(1, len(seq) - 1):
        if seq[i - 1] == seq[i + 1] and seq[i] != seq[i - 1]:
            seq[i] = seq[i - 1]
    return seq


cap = cv2.VideoCapture('movie.mp4')

sequence_r = []
sequence_g = []
sequence_b = []
min_cluster_area = 500  # minimum contiguous pixel cluster to count as LED on

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output_masked.mp4', fourcc, fps, (width, height))
out_hsv = cv2.VideoWriter('output_hsv.mp4', fourcc, fps, (width, height))


while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hsv_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out_hsv.write(hsv_bgr)

    # Red (wraps around 180°, needs two ranges)
    lower_redA = np.array([0, 100, 45])
    upper_redA = np.array([15, 255, 255])
    lower_redB = np.array([165, 100, 45])
    upper_redB = np.array([180, 255, 255])
    mask_r = cv2.inRange(hsv, lower_redA, upper_redA) | cv2.inRange(hsv, lower_redB, upper_redB)

    # Green
    lower_green = np.array([40, 80, 40])
    upper_green = np.array([80, 255, 255])
    mask_g = cv2.inRange(hsv, lower_green, upper_green)

    # Blue
    lower_blue = np.array([100, 150, 80])
    upper_blue = np.array([140, 255, 255])
    mask_b = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((3, 3), np.uint8)
    mask_r = cv2.morphologyEx(mask_r, cv2.MORPH_OPEN, kernel)
    mask_r = cv2.morphologyEx(mask_r, cv2.MORPH_CLOSE, kernel)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_OPEN, kernel)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, kernel)
    mask_b = cv2.morphologyEx(mask_b, cv2.MORPH_OPEN, kernel)
    mask_b = cv2.morphologyEx(mask_b, cv2.MORPH_CLOSE, kernel)

    combined_mask = mask_r | mask_g | mask_b
    result = cv2.bitwise_and(frame, frame, mask=combined_mask)
    out.write(result)

    area_r = largest_cluster_area(mask_r)
    area_g = largest_cluster_area(mask_g)
    area_b = largest_cluster_area(mask_b)

    # R and B should never be on simultaneously (permanent fault alternates).
    # During LED fade transitions both masks can exceed the threshold, so resolve
    # by keeping only the dominant channel (larger pixel area).
    r_on = area_r > min_cluster_area
    b_on = area_b > min_cluster_area
    if r_on and b_on:
        r_on = area_r >= area_b
        b_on = not r_on

    sequence_r.append(1 if r_on else 0)
    sequence_g.append(1 if area_g > min_cluster_area else 0)
    sequence_b.append(1 if b_on else 0)

out.release()
out_hsv.release()
cap.release()
cv2.destroyAllWindows()

# Strip leading silence and denoise each channel
sequence_r = flip_correct(remove_leading_zeros(remove_short_on_runs(sequence_r)))
sequence_g = flip_correct(remove_leading_zeros(remove_short_on_runs(sequence_g)))

sequence_b = flip_correct(remove_leading_zeros(remove_short_on_runs(sequence_b)))

list_result_r, time_sequence_r = build_time_sequence(sequence_r, fps)
list_result_g, time_sequence_g = build_time_sequence(sequence_g, fps)
list_result_b, time_sequence_b = build_time_sequence(sequence_b, fps)

print("FPS:", fps)
print("R runs:", list_result_r)
print("G runs:", list_result_g)
print("B runs:", list_result_b)
print("R time sequence:", time_sequence_r)
print("G time sequence:", time_sequence_g)
print("B time sequence:", time_sequence_b)

matched_state, score = match_sequence(time_sequence_r, time_sequence_g, time_sequence_b)
print(f"\nMatched state: {matched_state}  (DTW score: {score:.4f})")
