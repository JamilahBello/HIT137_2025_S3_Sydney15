import cv2
from image_model import ImageModel
from datetime import datetime

"""
Controller yaer in MVC.

Delegates all image logic and persistance to the model
Decides when changes should be commited or discarded
"""


class ImageController:

    def __init__(self, model: ImageModel):
        self.model = model
        self.img = None

    # Open an image via the model and initialise dummy image
    def open(self, path):
        self.model.open(path)
        self.img = self.model.get_current()

    # Get details about the image
    def get_details(self):
        self.model.get_details()

    # Undo last commited change
    def undo(self):
        self.img = self.model.undo()

    # Redo lsst undone commited change
    def redo(self):
        self.img = self.model.redo()

    # Apply grayscale to dummy image
    def grayscale(self):
        self.img = self.model.grayscale(self.img)

    # Apply gaussian blur to dummy image
    def blur(self, intensity):
        self.img = self.model.blur(self.img, intensity)

    # Apply canny edge detection to dummy image
    def canny_edges(self):
        self.img = self.model.canny_edges(self.img)

    # Apply brightness to dummy image
    def brightness(self, delta):
        self.img = self.model.brightness(self.img, delta)

    # Apply contrast to dummy image
    def contrast(self, alpha):
        self.img = self.model.contrast(self.img, alpha)

    # Rotate dummy image
    def rotate(self, angle):
        self.img = self.model.rotate(self.img, angle)

    # Flip to dummy image horizontally or vertically
    def flip(self, mode):
        self.img = self.model.flip(self.img, mode)

    # Resize dummy image
    def resize(self, width=None, height=None):
        self.img = self.model.resize(self.img, width, height)

    # Save Image
    def save(self):
        now = str(int(datetime.now().timestamp() * 1000))
        self.model.save(f"image_{now}.jpg")

    # Save Image with specific name and filetype
    def saveAs(self, name, filetype):
        self.model.save(f"{name}.{filetype}")

    # Commit transformation
    def ok(self):
        self.model.set_current(self.img)

    # Cancel transformation
    def cancel(self):
        self.img = self.model.get_current()

    # Reset to original condition
    def reset(self):
        self.img = self.model.reset()
