import cv2
from API.ConsumoApi import gerarimagem

class Camera:
	def __init__(self, device_index = 0):
		self.device_index = device_index
		self.camera = cv2.VideoCapture(self.device_index)

		if not self.camera.isOpened():
			raise IOError(f"Can-not open camera with index {self.device_index}")
		print(f"Camera {self.device_index} initialized and ready.")

	def capture_photo(self, filename="photo.jpg"):
		ret, frame = self.camera.read()
		if ret:
			cv2.imwrite(filename, frame)
			gerarimagem(filename)

			print(f"Photo saved as {filename}")
		else: print("Failed to capture image.")

	def release_camera(self):
		if self.camera.isOpened():
			self.camera.release()
			print("Camera released.")
