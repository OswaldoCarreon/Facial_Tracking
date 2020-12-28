import cv2
import time

# Load the cascade
face_cascade = cv2.CascadeClassifier('../assets/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX


def exit(camara):
    camara.release()


def getFaces(camara,neighbors,scale):
    _, frame = camara.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame, face_cascade.detectMultiScale(gray, scale, neighbors)


def detectingFaces(neighbors,scale):
    x1 = x2 = y1 = y2 = 0
    camara = cv2.VideoCapture(0)

    while True:
        frame, faces = getFaces(camara,neighbors,scale)
       
        #print(f" Faces object = {faces}, Type = {type(faces)}")
        for (x, y, w, h) in faces:
            x1 = x
            x2 = w
            y1 = y1
            y2 = h
            print(f"Coordinates = {x}, {y}, {w}, {h}")
            cv2.rectangle(frame, (x, y), (x+w, y+h), (130, 224, 170), 2)
        # Display
        
        info = "Neigh = {}, Scale = {}, coordinates = ({}, {}, {}, {} )".format(neighbors,scale,x1,x2,y1,y2)

        cv2.putText(frame, info, (10,20), font, 0.5, (53,67,203), 2)
        cv2.imshow('frame', frame)
     
        key = cv2.waitKey(1) & 0xFF     
      
        if key == ord("q"):
            exit(camara)

        if cv2.waitKey(33) == ord('a'):
            if neighbors <= 0:
                neighbors = 0
            else:
                neighbors -= 1

        if cv2.waitKey(33) == ord('d'):
            neighbors += 1

        if cv2.waitKey(33) == ord('s'):
            if scale <= 1.1:
                scale = 1.1
            else:
                scale -= .1

        if cv2.waitKey(33) == ord('w'):
            if scale >= 1.9:
                scale = 1.9
            else:
                scale += .1


if __name__ == "__main__":
    print("FACE TRACKING STARTED...")
    neighbors = 4
    scale = 1.1
    detectingFaces(neighbors,scale)
