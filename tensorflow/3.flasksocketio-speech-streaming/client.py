import speech_recognition as sr
import base64
from socketIO_client import SocketIO, BaseNamespace
from threading import Thread, ThreadError
import time

socketIO = SocketIO('localhost',5000)
live_namespace = socketIO.define(BaseNamespace, '/live')

def receive_events_thread():
    socketIO.wait()
def on_speech_response(*args):
    print(args[0])

live_namespace.on('speech_update', on_speech_response)
receive_events_thread = Thread(target=receive_events_thread)
receive_events_thread.daemon = True
receive_events_thread.start()

r = sr.Recognizer()
r.energy_threshold = 10000
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    #with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! sending to server..")
        try:
            print(len(audio.frame_data))
            if len(audio.frame_data) < 100000:
                print('too short, skip')
                time.sleep(0.5)
                continue
            base64_bytes = base64.b64encode(audio.frame_data)
            base64_string = base64_bytes.decode('utf-8')
            live_namespace.emit('livespeech',{'data':base64_string,'sample_rate':audio.sample_rate,'sample_width':audio.sample_width})
        except:
            pass
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
