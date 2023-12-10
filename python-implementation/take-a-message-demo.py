import signal
from gpiozero import Button,LED
import time
import pyaudio
import wave



BANNER = """
    ___       _______   ________  ___      ___ _______           ________          _____ ______   _______   ________   ________  ________  ________  _______      
    |\  \     |\  ___ \ |\   __  \|\  \    /  /|\  ___ \         |\   __  \        |\   _ \  _   \|\  ___ \ |\   ____\ |\   ____\|\   __  \|\   ____\|\  ___ \     
    \ \  \    \ \   __/|\ \  \|\  \ \  \  /  / | \   __/|        \ \  \|\  \       \ \  \\\__\ \  \ \   __/|\ \  \___|_\ \  \___|\ \  \|\  \ \  \___|\ \   __/|    
     \ \  \    \ \  \_|/_\ \   __  \ \  \/  / / \ \  \_|/__       \ \   __  \       \ \  \\|__| \  \ \  \_|/_\ \_____  \\ \_____  \ \   __  \ \  \  __\ \  \_|/__  
      \ \  \____\ \  \_|\ \ \  \ \  \ \    / /   \ \  \_|\ \       \ \  \ \  \       \ \  \    \ \  \ \  \_|\ \|____|\  \\|____|\  \ \  \ \  \ \  \|\  \ \  \_|\ \ 
       \ \_______\ \_______\ \__\ \__\ \__/ /     \ \_______\       \ \__\ \__\       \ \__\    \ \__\ \_______\____\_\  \ ____\_\  \ \__\ \__\ \_______\ \_______\
        \|_______|\|_______|\|__|\|__|\|__|/       \|_______|        \|__|\|__|        \|__|     \|__|\|_______|\_________\\_________\|__|\|__|\|_______|\|_______|
                                                                                                               \|_________\|_________|                             
                                                                                                                                                                
    TM
"""

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 60 * 10 # 10 min max


def test_main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    waveFile = None
    def on():
        print("recording...")
        frames = []
        stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")
        pass
    def off():
        # stop Recording
        stream.stop_stream()
        
        waveFile = wave.open(recording_filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
    print(BANNER)
    btn = Button(4,bounce_time=.05)
    btn.when_pressed = on
    btn.when_released = off
    while True:
        pass




def main():
    print(BANNER)
    btn = Button(4,bounce_time=.05)
    btn.when_released = off
    led = LED(2)
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    waveFile = None
    # Close if control C
    def handler(signum, frame):
        stream.close()
        audio.terminate()
        if waveFile:
            waveFile.close()        
        exit(1)
    signal.signal(signal.SIGINT, handler)

    while True:
        btn.wait_for_press(timeout=None)
        END_STREAM = False
        led.on()
        print("switch is on!")
        time_string = time.strftime("%Y%m%d-%H%M%S")
        recording_filename = f"leave-a-message-{time_string}.wav"
        print(f"Audio is being recorded to:{recording_filename}")

        print("recording...")
        frames = []
        stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if END_STREAM:
                break
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")
        
        # stop Recording
        stream.stop_stream()
        
        waveFile = wave.open(recording_filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        led.off()
        print("switch is off!")


if __name__ == "__main__":
    main()