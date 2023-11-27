from gpiozero import Buttons,LED
import wave
import time
import sys
import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5



def main():
    btn = Button(4)
    while True:
        btn.wait_for_press()
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