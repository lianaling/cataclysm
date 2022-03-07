import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
from bot import bot
from cnn import IMG_SIZE, model
from datetime import datetime
from threading import Thread
import os
from dotenv import load_dotenv
import tensorflow as tf

# Load env var
load_dotenv()
CAM_URL = os.getenv('CAM_URL')
CHAT_ID = int(os.getenv('CHAT_ID'))

# Constant
IMG_SIZE = 50

# Global var between threads
filename = 'image.jpg'
dt = datetime.today()
q_th = []

def detect_cat():
    # IP Cam
    cap = cv2.VideoCapture(CAM_URL)

    # Send start message
    bot.send_message(text=f'Cat Detector Started {dt}', chat_id=CHAT_ID)

    while True:
        _, frame = cap.read()
        if frame is not None:
            # bot.send_message(text=f'Frame resolution {frame.shape}', chat_id=CHAT_ID)
            data = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            gray_frame = tf.reshape(data, (1,50,50,1))
            frame = cv2.resize(gray_frame, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)

            # data = frame.reshape(IMG_SIZE, IMG_SIZE, 1)
            faces = model.predict([frame])[0]

            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            ax.imshow(frame, cmap="gray")

            if faces[1] > faces[0]:
                print("No cat faces found")

            else:
                print(f"Probability of cat face: {faces[0]}")

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