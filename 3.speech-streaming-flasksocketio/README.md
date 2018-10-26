## Installation
```bash
apt-get install portaudio19-dev
pip3 install flask flask_socketio numpy SpeechRecognition pyaudio
```

## How-To

`client.py` is your microphone slave.

`server.py` is your server to process the speech. In this case, I use google Speech-to-Text.

1. Run the server,
```bash
python3 server.py
```
```text
127.0.0.1 - - [26/Oct/2018 12:40:12] "GET /socket.io/?t=1540528811038-30&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:13] "POST /socket.io/?t=1540528813056-33&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:13] "GET /socket.io/?t=1540528812056-32&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:14] "POST /socket.io/?t=1540528814074-35&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:14] "GET /socket.io/?t=1540528813074-34&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:15] "POST /socket.io/?t=1540528815091-37&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:40:15] "GET /socket.io/?t=1540528814091-36&EIO=3&transport=polling&sid=842d33cc0b354a7b8e631d519fc7d41a HTTP/1.1" 200 -
Client disconnected

```

2. Run the client,
```bash
python3 client.py
```
```text
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
A moment of silence, please...
Set minimum energy threshold to 10000
Say something!
Got it! sending to server..
157696
{'text': 'Hello'}
Say something!
Got it! sending to server..
194560
{'text': 'sayang busuk'}
Say something!
```
