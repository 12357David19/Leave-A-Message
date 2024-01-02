from gpiozero import Button,LED





def main():
    


    btn = Button(4,bounce_time=.01)
    led = LED(21)
    def on(button):
        led.on()
        print("switch is on!")

    def off(button):
        led.off()
        print("switch is off\n")
    btn.when_pressed = on
    btn.when_released = off
    while True:
        pass
if __name__ == "__main__":
    main()