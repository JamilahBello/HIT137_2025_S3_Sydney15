import cv2
from image_model import ImageModel
from datetime import datetime


class ImageController:

    def __init__(self, model: ImageModel):
        self.model = model
        self.img = None

    def open(self, path):
        self.model.open(path)
        self.img = self.model.get_current()

    def get_details(self):
        self.model.get_details()

    def undo(self):
        self.img = self.model.undo()

    def redo(self):
        self.img = self.model.redo()

    def grayscale(self):
        self.img = self.model.grayscale(self.img)

    def blur(self, intensity):
        self.img = self.model.blur(self.img, intensity)

    def canny_edges(self):
        self.img = self.model.canny_edges(self.img)

    def brightness(self, delta):
        self.img = self.model.brightness(self.img, delta)

    def contrast(self, alpha):
        self.img = self.model.contrast(self.img, alpha)

    def rotate(self, angle):
        self.img = self.model.rotate(self.img, angle)

    def flip(self, mode):
        self.img = self.model.flip(self.img, mode)

    def resize(self, width=None, height=None):
        self.img = self.model.resize(self.img, width, height)

    def save(self):
        now = str(int(datetime.now().timestamp() * 1000))
        self.model.save(f"image_{now}.jpg")

    def saveAs(self, name, filetype):
        self.model.save(f"{name}.{filetype}")

    def ok(self):
        self.model.set_current(self.img)

    def cancel(self):
        self.img = self.model.get_current()

    def reset(self):
        self.img = self.model.reset()
