import cv2
import numpy as np
import imutils
from bot import bot
from datetime import datetime
from threading import Thread
import os

url = 'http://192.168.1.24:8080/video'
xml = 'C:/Users/liana/Documents/Projects/cat-detector/haarcascade_frontalcatface.xml'
filename = 'image.jpg'
dt = datetime.today()
chat_id = 1088156959

q_th = []

def detect_cat(url: str, xml: str):

    # IP Cam

    cap = cv2.VideoCapture(url)

    # Get image classifier
    catFaceCasacde = cv2.CascadeClassifier(xml)

    # Send start message
    bot.send_message(text=f'Cat Detector Started {dt}', chat_id=chat_id)

    while True:
        cam, frame = cap.read()
        if frame is not None:
            frame = imutils.resize(frame, width=680)

            faces = catFaceCasacde.detectMultiScale(frame)

            # Number of lines of the matrix corresponds to number of faces detected
            if len(faces) == 0:
                print("No cat faces found")

            else:
                print(f"Number of cat faces detected: {faces.shape[0]}")

                # Draw faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))

                if len(q_th) == 0:
                    q_th.append(frame)

            cv2.imshow('Frame', frame)

        q = cv2.waitKey(1)
        if q == ord('q'):
            os._exit(1)

    cv2.destroyAllWindows()

    bot.send_message(text=f'Cat Detector Terminated {dt}', chat_id=1088156959)

def write_cat():
    while True:
        if len(q_th) != 0:
            cv2.imwrite(filename, q_th[0])
            bot.send_message(text=f'CAT ALERT {dt}', chat_id=chat_id)
            bot.send_photo(photo=open(filename, 'rb'), chat_id=chat_id)
            q_th.clear()

if __name__ == "__main__":
    read_th = Thread(target=detect_cat, args=(url, xml))
    write_th = Thread(target=write_cat, args=())

    # Start
    read_th.start()
    write_th.start()

    # Wait for completion
    read_th.join()
    write_th.join()