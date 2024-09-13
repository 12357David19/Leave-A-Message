import RPi.GPIO as GPIO
import time
import os

# Variables
butPressed = True  # True if the button is pressed, then butPressed[i] is False
pin = [4]  # GPIO pins of each button
recordBool = False  # True if a record is in progress
stopRecordingDelay = 1.5  # Time in seconds to confirm the button release to stop recording
debounceTime = 0.05  # 50 milliseconds debounce time

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Sets Pi's internal resistors to pull-up

while True:
    butPressed = GPIO.input(pin[0])  # Checks if a button is pressed

    # Debouncing check: wait for debounce time and check the button state again
    if not butPressed:  # If a button is pressed
        time.sleep(debounceTime)  # Debounce delay
        if not GPIO.input(pin[0]):  # Confirm the button is still pressed after debounce time
            press_start_time = time.time()
            while not GPIO.input(pin[0]) and not recordBool:
                # Check continuously while button is pressed
                if time.time() - press_start_time > 1.0:  # If the button is pressed for more than a second, then recordBool is True
                    recordBool = True

            if recordBool:  # If recordBool is True, it starts recording
                print("Recording")
                os.system("arecord test.wav -D sysdefault:CARD=1 -f cd -d 20 &")  # Records for a maximum of 20 seconds

                # Wait for button release
                release_time = None  # Initialize release time to None
                while True:
                    if GPIO.input(pin[0]):  # If button is released
                        if release_time is None:  # Set release time if it hasn't been set yet
                            release_time = time.time()
                        
                        # Check if button remains released continuously for stopRecordingDelay
                        if time.time() - release_time >= stopRecordingDelay:
                            print("No longer recording")
                            os.system("pkill -9 arecord")  # Stop the recording
                            recordBool = False
                            break
                    else:
                        # Reset release time if button is pressed again
                        release_time = None
                    
                    time.sleep(0.1)  # Short delay to avoid high CPU usage

    time.sleep(0.1)
