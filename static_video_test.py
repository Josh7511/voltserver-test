import numpy as np
import cv2

cap = cv2.VideoCapture('movie.mp4')

sequence = []
list_result = [[]]
time_sequence = []
min_led_area = 30

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output_masked.mp4', fourcc, fps, (width, height))
# HSV visualization video (no mask applied)
out_hsv = cv2.VideoWriter('output_hsv.mp4', fourcc, fps, (width, height))


while True:
    ret, frame = cap.read()
    if not ret:
        break
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Save full HSV image (converted back to BGR for viewing) without any mask
    hsv_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    out_hsv.write(hsv_bgr)

    # Looser red bounds so compression/lighting shifts don't drop the LED in/out
    lower_redA = np.array([0, 100, 45])
    upper_redA = np.array([15, 255, 255])
    lower_redB = np.array([165, 100, 45])
    upper_redB = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_redA, upper_redA) | cv2.inRange(hsv, lower_redB, upper_redB)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    fps = cap.get(cv2.CAP_PROP_FPS)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    out.write(result)


    if np.sum(mask) > min_led_area:
        sequence.append(1)
    else:
        sequence.append(0)

    
    
out.release()
out_hsv.release()

# Correct single isolated bit flips (one-off noise)
for i in range(1, len(sequence) - 1):
    if sequence[i - 1] == sequence[i + 1] and sequence[i] != sequence[i - 1]:
        sequence[i] = sequence[i - 1]

#stores sequences into subseqeunces
for i in range(len(sequence)):
    if i > 0 and (sequence[i-1] == 0 and sequence[i] == 1 or sequence[i-1] == 1 and sequence[i] == 0):
        list_result.append([])
    list_result[-1].append(sequence[i])
    print(sequence[i], end="")

# calucaltes time of each sequence
for list in list_result:
    time_sequence.append(len(list)/fps)

print(" ")
print("FPS: ", fps)
print("result:", list_result)
print("time sequence:", time_sequence)

cap.release()
cv2.destroyAllWindows()