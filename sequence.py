#Note each sequence starts with LED on currently, may have to update program since PERM Fault is alternating
#Note sequences are in the follow format [on_1, off_1, on_2, off_2, ...] in seconds.

BLINK_SEQUENCES = {
    "Init": {
        # B  100 ms @ 50 %
        "R": [],
        "G": [],
        "B": [0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    },
    "Wait 1": {
        # G  500 ms @ 50 %, show 1/4  →  1 pulse then 3-slot gap
        "R": [],
        "G": [0.25, 1.75, 0.25, 1.75, 0.25, 1.75],
        "B": [],
    },
    "Wait 2": {
        # G  500 ms @ 50 %, show 2/4  →  2 pulses then 2-slot gap
        "R": [],
        "G": [0.25, 0.25, 0.25, 1.25, 0.25, 0.25, 0.25, 1.25],
        "B": [],
    },
    "Wait 3": {
        # G  500 ms @ 50 %, show 3/4  →  3 pulses then 1-slot gap
        "R": [],
        "G": [0.25, 0.25, 0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.75],
        "B": [],
    },
    "Precharge": {
        # G  100 ms @ 50 %
        "R": [],
        "G": [0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
        "B": [],
    },
    "Full On": {
        # G solid (100 %), B  3 s @ 0.2 %  →  6 ms on / 2994 ms off
        "R": [],
        "G": [9],
        "B": [0.006, 2.994, 0.006, 2.994, 0.006, 2.994],
    },
    "Software Off": {
        # B  3 s @ 0.2 %  →  6 ms on / 2994 ms off
        "R": [],
        "G": [],
        "B": [0.006, 2.994, 0.006, 2.994, 0.006, 2.994],
    },
    "Fault Delay": {
        # R  500 ms @ 20 %  with 1 s off-guard before & after
        # → 100 ms on, 400 ms off + 1 s guard = 1400 ms off
        "R": [0.1, 0.4, 0.1, 0.4, 0.1, 0.4, 0.1, 1.4],
        "G": [],
        "B": [],
    },
    "Permanent Fault": {
        # R/B  200 ms @ 50 %  alternating
        # Each color: 100 ms on, 100 ms off (while the other color is on)
        "R": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        "G": [],
        "B": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    },
    "Live ID": {
        # B  1000 ms @ 25 %  →  250 ms on / 750 ms off
        "R": [],
        "G": [],
        "B": [0.25, 0.75, 0.25, 0.75, 0.25, 0.75, 0.25, 0.75],
    },
}
