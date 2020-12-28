from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

thresholdVariable = 200
minSize = 700

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="/")
ap.add_argument("-a", "--min-area", type=int, default=minSize, help="minimum area size")
args = vars(ap.parse_args())


if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)


else:
	vs = cv2.VideoCapture(args["video"])


firstFrame = None


while True:
	#Obteniendo el frame de la camara
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unfinished"


	if frame is None:
		break


	#-------------------------------------------------------------------------------

	#Ajustando el frame de tamaño y de color a escala de grises.
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue


	#-------------------------------------------------------------------------------
	#Comparando el primer frame con el frame leído para ver si hubo un cambio.
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, thresholdVariable, 255, cv2.THRESH_BINARY)[1]


	#-------------------------------------------------------------------------------
	# Dilatando la diferencia y obteniendo los contornos de de lo obtenido
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	

	#-------------------------------------------------------------------------------
	#Si los contornos no pasan el filtro del tamaño, entonces ignoro el objeto, si no, entonces dibujo los contornos.
	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue

		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Fished"


	#-------------------------------------------------------------------------------
	# Dibujando todo el el frame.
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
	cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break


# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()