import numpy as np
import cv2

cap = cv2.VideoCapture(1)

sequence = []
list_result = [[]]
time_sequence = []




while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_redA = np.array([0, 180, 45]) 
    upper_redA = np.array([10, 255, 255])
    lower_redB = np.array([170, 180, 45])
    upper_redB = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_redA, upper_redA) | cv2.inRange(hsv, lower_redB, upper_redB)
    fps = cap.get(cv2.CAP_PROP_FPS)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', result)
    cv2.imshow('mask', mask)

    if np.sum(mask) > 0:
        sequence.append(1)
    else:
        sequence.append(0)

    if cv2.waitKey(1) == ord('q'):
        for i in range(len(sequence)):
            if i > 0 and (sequence[i-1] == 0 and sequence[i] == 1 or sequence[i-1] == 1 and sequence[i] == 0):
                list_result.append([])
            list_result[-1].append(sequence[i])
            print(sequence[i], end="")
        for list in list_result:
            time_sequence.append(len(list)/fps)
        print(" ")
        print("FPS: ", fps)
        print("result:", list_result)
        print("time sequence:", time_sequence)
        break

cap.release()
cv2.destroyAllWindows()