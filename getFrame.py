
import cv2

INPUT_FILE='input_encode.avi'
FRAME_NUMBER=70

cap=cv2.VideoCapture(INPUT_FILE)
cap.set(cv2.CAP_PROP_POS_FRAMES, FRAME_NUMBER)
ret,frame=cap.read()
cv2.imwrite("frame_"+INPUT_FILE+".png",frame)
