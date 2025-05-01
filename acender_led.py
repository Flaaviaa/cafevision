from gpiozero import LED

class ChangeLedState:
	def __init__(self, led_pin=17):
		self.led = LED(led_pin)
		self.led_state = False

	def change_led_state(self):
		if self.led_state:
			self.led.off()
		else:
			self.led.on()
		self.led_state = not self.led_state
