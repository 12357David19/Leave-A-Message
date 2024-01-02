from gpiozero import Button,LED
import wave
import time
import sys
import pyaudio
import multiprocessing
import signal


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
# Shared variable to control audio recording
record_audio_flag = multiprocessing.Value('b', True)



def listen_for_button(button: Button):
    global record_audio_flag
    button.wait_for_release(timeout=300)
    print("switch is off!")
    with record_audio_flag.get_lock():
        record_audio_flag.value = False     


def record_audio():
    global record_audio_flag

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    # RECORD_SECONDS = 10
    time_string = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = f"leave-a-message-{time_string}.wav"
    print(f"Audio is being recorded to:{recording_filename}")
    
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
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
    with wave.open(recording_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"Audio recorded: {recording_filename}")


    pass





def main():
    def signal_handler(sig, frame):
        global record_audio_flag
        print(f"Received signal {sig}. Exiting.")
        with record_audio_flag.get_lock():
            record_audio_flag.value = False
        

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)


    print(BANNER)
    btn = Button(4,bounce_time=.05)
    # led = LED(2)
    while True:
        button_process = multiprocessing.Process(target=listen_for_button,args=(btn,))
        audio_process = multiprocessing.Process(target=record_audio)
        # Wait for button to be pressed
        btn.wait_for_press(timeout=None)
        # After button pressed listen for release and start recording
        button_process.start()
        audio_process.start()

        try:
            # Wait for processes to finish before exiting
            button_process.join()
            audio_process.join()
        except KeyboardInterrupt:
            print("Ctrl+C pressed. Waiting for processes to complete...")
            button_process.terminate()
            audio_process.terminate()
            button_process.join()
            audio_process.join()
    
if __name__ == "__main__":
    main()