import numpy as np
import cv2

cap = cv2.VideoCapture(1)

sequence = []


while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 180, 45]) 
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', result)
    cv2.imshow('mask', mask)

    if cv2.countNonZero(mask) > 0:
        sequence.append(1)
    else:
        sequence.append(0)

    if cv2.waitKey(1) == ord('q'):
        for i in sequence:
            print(sequence[i], end="")
        break

cap.release()
cv2.destroyAllWindows()