from signal import pause
from button_handler import ButtonHandler

system = ButtonHandler(button_pin = 27, led_pin = 17, device_index = 0)
pause()

