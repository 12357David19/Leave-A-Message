from gpiozero import Button,LED
import wave
import time
import sys
import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

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




def main():
    print(BANNER)
    btn = Button(4,bounce_time=.05)
    led = LED(2)
    while True:
        btn.wait_for_press(timeout=None)
        led.on()
        print("switch is on!")
        time_string = time.strftime("%Y%m%d-%H%M%S")
        recording_filename = f"leave-a-message-{time_string}.wav"
        print(f"Audio is being recorded to:{recording_filename}")
        
        frames = []
        def callback(in_data, frame_count, time_info, status):
            data = stream.readframes(frame_count)
            frames.append(data)
            return (data, pyaudio.paContinue)
        
        p = pyaudio.PyAudio()

        # Open stream using callback (3)
        # TODO: Not sure what input channel number it will be
        stream = p.open(format=FORMAT,
                        input_device_index = 2,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)
        
        print("recording...")

        # Wait for stream to finish (4)
        # Timeout of 5 minutes (For now)
        btn.wait_for_release(timeout=300)  
        print("switch is off!")      
        # Close the stream (5)
        stream.close()
        # Release PortAudio system resources (6)
        p.terminate()
        # Record audio to WAV
        with wave.open(recording_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"Audio recorded: {recording_filename}")

if __name__ == "__main__":
    main()