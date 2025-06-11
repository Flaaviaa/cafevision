from gpiozero import LED
import time

class ChangeLedState:
    def __init__(self, led_pin=26):  # Usando GPIO26
        self.led = LED(led_pin)
        self.led_state = False

    def change_led_state(self):
        if self.led_state:
            self.led.off()
        else:
            self.led.on()
        self.led_state = not self.led_state

if __name__ == "__main__":
    led_controller = ChangeLedState(26)  # GPIO26
    while True:
        led_controller.change_led_state()
        time.sleep(1)  # Pisca o LED a cada 1 segundo
