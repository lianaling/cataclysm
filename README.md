## Cat Detector

To detect cats and alert through Telegram.

### Setup
1. Clone repo
2. `pip install opencv-python python-telegram-bot python-dotenv`
3. [Download `IP Webcam` on Android phone](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en&gl=US)
4. Get CAM_URL (append `/video` after the IP address)
5. Subscribe to `CatSiren` bot on Telegram (username: `@CatSirenBot`)
6. [Send a message to get `CHAT_ID`](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API)
7. Create `.env` file

Note: Press `Q` while being on the camera active window to quit the program.

### Things for improvement:
- Cat face detection algorithm: to detect the entire cat body instead of frontal face
- Add user controls from Telegram client
- Deploy application
