## Installation
```bash
apt-get install portaudio19-dev
pip3 install flask flask_socketio numpy SpeechRecognition pyaudio
```

## How-To

`client.py` is your microphone slave.

`server.py` is yout server to process the speech. In this case, I use google Speech-to-Text.

1. Run the server,
```bash
python3 server.py
```

2. Run the client,
```bash
python3 client.py
```
