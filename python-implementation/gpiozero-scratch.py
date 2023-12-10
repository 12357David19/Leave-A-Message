from gpiozero import Button,LED


def on():
    led = LED(2)
    led.on()
    print("switch is on!")

def off():
    led = LED(2)
    led.off()
    print("switch is off")


def main():
    


    btn = Button(4)

    btn.when_pressed = on
    btn.when_released = off
    while True:
        pass
if __name__ == "__main__":
    main()