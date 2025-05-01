from gpiozero import Button
from acender_led import ChangeLedState
from camera import Camera
from time import sleep

class ButtonHandler:
	def __init__(self, button_pin = 27, led_pin = 17, device_index = 0):
		self.led_controller = ChangeLedState(led_pin)
		self.camera = Camera(device_index)
		self.button = Button(button_pin)
		self.button.when_pressed = self.handle_button_press

	def handle_button_press(self):
		self.led_controller.change_led_state()
		if self.led_controller.led_state:
			for i in range(1, 4):
				filename = f"photo_{i}.png"
				self.camera.capture_photo(filename)
				sleep(1)
				print(f"Photo {filename} initialized and ready.")

	def release_resources(self):
		self.camera.release_camera()
