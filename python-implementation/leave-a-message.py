from gpiozero import Button,LED
import time
import multiprocessing
import signal
import os

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
    stop_audio_sep_prog()
    record_audio_sep_prog()

def record_audio_sep_prog():
    print("Recording")
    time_string = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = f"leave-a-message-{time_string}.wav"
    os.system(f"arecord /home/dav/Documents/coding/python/Leave-A-Message/python-implementation/wavs/{recording_filename} -D sysdefault:CARD=1 -f cd -d 20 &")  # Records for a maximum of 20 seconds
    
def stop_audio_sep_prog():
    print("Stopping")
    os.system("pkill -9 arecord")  # Stop the recording

def off():
    # stop_audio()
    stop_audio_sep_prog()
    led.off()

def main():
    print(f"Starting software")
    btn = Button(4,pull_up=True)

    btn.when_pressed = on
    btn.when_released = off
    while True:
        pass
if __name__ == "__main__":
    main()