from imutils.video import FPS
import numpy as np
import imutils
import cv2
import time
FILE_NAME="../test/720.mp4"
CONFIDENCE=0.50
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
vs = cv2.VideoCapture(FILE_NAME)
writer = None
fps = FPS().start()
flen = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
print("FRAMES: "+str(flen))
nprocessed=0
stTime=time.time()
f1=open("modFile.txt","w")
while True:
	st = time.time();
	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# resize the frame, grab the frame dimensions, and convert it to
	# a blob
	##frame = imutils.resize(frame, width=400)
	(h, w) = frame.shape[:2]
	# blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	nprocessed += 1
	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > CONFIDENCE:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			# label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			str1 = str(startX) + " " + str(startY) + " " + str(endX) + " " + str(endY)
			f1.write(str1 + "\n")
			y = startY - 15 if startY - 15 > 15 else startY + 15
			# cv2.putText(frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	str1="!\n"
	f1.write(str1)

	# check to see if the output frame should be displayed to our
	# screen
	# show the output frame
	ed = time.time()
	print("\r" + str(nprocessed) + " time: " + str(ed - st), end="")
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	fps.update()
	end=time.time()
	print("\r"+str(end-stTime),end="");

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))