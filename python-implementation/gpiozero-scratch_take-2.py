from gpiozero import Buttons,LED





def main():
    btn = Button(4)
    while True:
        btn.wait_for_press(timeout=None)
        print("switch is on!")
        time_string = time.strftime("%Y%m%d-%H%M%S")
        recording_filename = f"leave-a-message-{time_string}.wav"
        print(f"Audio is being recorded to:{recording_filename}")

        btn.wait_for_release(timeout=300)  
        print("switch is off!")

if __name__ == "__main__":
    main()