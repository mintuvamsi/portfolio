import cv2, os
import sys
from time import sleep


cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
cascpath = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
facecascade = cv2.CascadeClassifier(cascpath)

video_capture = cv2.VideoCapture(0)
anterior = 0 

while True:
    if not video_capture.isOpened():
        print("Unable to read camera feed")
        sleep(5)
        pass

    #Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(gray, 
                                         scaleFactor=1.1, 
                                         minNeighbors=5, 
                                         minSize=(30, 30))
    
    for i,(x,y,w,h) in enumerate(faces):
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
        face = frame[y:y+h,x:x+w]
        cv2.imwrite(f'face{i}.jpg', face)

    if anterior !=len(faces):
        anterior = len(faces)

    #Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release capture
video_capture.release()
cv2.destroyAllWindows()