## Project Cataclysm

To detect cats using cat face detection with haar cascades classifier and alert user through Telegram.

<br/>

Once running, the `Cataclysm` bot will alert you through Telegram that f`f"Cataclysm Started {timestamp}"` with a timestamp.

<br/>

When it detects a cat, it will send `f"CAT ALERT {timestamp}"`.

<br/>

Upon termination, it will send `f"Cataclysm Terminated {timestamp}"`.


### Setup
1. Clone repo
2. `pip install opencv-python python-telegram-bot python-dotenv`
3. [Download `IP Webcam` on Android phone](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US)
4. Get CAM_URL (append `/video` after the IP address)
5. Subscribe to `Cataclysm` bot on Telegram (username: `@CatSirenBot`)
6. [Send a message to get `CHAT_ID`](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API)
7. Create `.env` file
8. Put phone outside

Note: Press `Q` while being on the camera active window to quit the program.

### Things for improvement:
- Cat face detection algorithm: to detect the entire cat body instead of frontal face (swap to CNN)
- Add user controls from Telegram client
- Deploy application
