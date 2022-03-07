import cv2
import numpy as np
import imutils
from bot import bot
from datetime import datetime
from threading import Thread
import os
from dotenv import load_dotenv

# Load env var
load_dotenv()
CAM_URL = os.getenv('CAM_URL')
CHAT_ID = int(os.getenv('CHAT_ID'))

# Global var between threads
xml = './haarcascade_frontalcatface.xml'
filename = 'image.jpg'
dt = datetime.today()
q_th = []

def detect_cat():
    # IP Cam
    cap = cv2.VideoCapture(CAM_URL)

    # Get image classifier
    catFaceCasacde = cv2.CascadeClassifier(xml)

    # Send start message
    bot.send_message(text=f'Cat Detector Started {dt}', chat_id=CHAT_ID)

    while True:
        _, frame = cap.read()
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

                # Push to queue
                if len(q_th) == 0:
                    q_th.append(frame)

            cv2.imshow('Frame', frame)

        # Exit
        q = cv2.waitKey(1)
        if q == ord('q'):
            bot.send_message(text=f'Cat Detector Terminated {dt}', chat_id=CHAT_ID)
            cv2.destroyAllWindows()
            os._exit(1)


def send_alert():
    while True:
        if len(q_th) != 0:
            cv2.imwrite(filename, q_th[0])
            bot.send_message(text=f'CAT ALERT {dt}', chat_id=CHAT_ID)
            bot.send_photo(photo=open(filename, 'rb'), chat_id=CHAT_ID)
            q_th.clear()

if __name__ == "__main__":
    read_th = Thread(target=detect_cat)
    write_th = Thread(target=send_alert)

    # Start
    read_th.start()
    write_th.start()

    # Wait for completion
    read_th.join()
    write_th.join()