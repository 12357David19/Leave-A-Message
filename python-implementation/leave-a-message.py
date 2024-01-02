from pathlib import Path
from gpiozero import Button,LED
import wave
import time
import sys
import pyaudio
import threading
import multiprocessing
import signal


# record_audio_flag = True
# lock = threading.Lock()
record_audio_flag = multiprocessing.Value('b', False)
recording_thread = None
led = LED(21)
def signal_handler(sig, frame):
    global led
    print(f"Received signal {sig}. Exiting.")
    led.off()
    exit(1)
# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def on():
    global record_audio_flag
    global recording_thread
    print("switch is on!")
    led.on()
    stop_audio()
    recording_thread = multiprocessing.Process(target=record_audio)
    recording_thread.start()

def record_audio():
    global record_audio_flag
    with record_audio_flag.get_lock():
        record_audio_flag.value = True 
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    # RECORD_SECONDS = 10
    time_string = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = f"leave-a-message-{time_string}.wav"
    print(f"Audio is being recorded to:{recording_filename}")
    
    audio = pyaudio.PyAudio()
    device_count = audio.get_device_count()
    for i in range(0, device_count):
        info = audio.get_device_info_by_index(i)
        print("Device {} = {}".format(info["index"], info["name"]))

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    input_device_index=8,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    while True:
        with record_audio_flag.get_lock():
            if not record_audio_flag.value:
                break
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("finished recording")
    
    # Saving to file
    print(f"Saving to WAV file: {recording_filename}.")
    recording_path = Path("/home/dav/Documents/coding/python/Leave-A-Message/python-implementation/wavs") / Path(recording_filename)
    with wave.open(recording_path.as_posix(), 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"Audio recorded: {recording_filename}")

def off():
    stop_audio()
    led.off()

def stop_audio():
    global recording_thread
    global record_audio_flag

    print("switch is off")
    with record_audio_flag.get_lock():
        if record_audio_flag.value == True:
            record_audio_flag.value = False
    if recording_thread:
        recording_thread.join()
def main():
    
    btn = Button(4)

    btn.when_pressed = on
    btn.when_released = off
    while True:
        pass
if __name__ == "__main__":
    main()