import cv2
from image_model import ImageModel
from datetime import datetime
from PIL import Image

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

    def get_display_pil(self):
        if self.img is None:
            return None
        if len(self.img.shape) == 2:
            return Image.fromarray(self.img)  # [22]

        rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)  # [21]
        return Image.fromarray(rgb)  # [22]

    def get_size(self):
        if self.img is None:
            return None

        h, w = self.img.shape[:2]  # [1]
        return w, h

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
        self.ok()

    # Apply gaussian blur to dummy image
    def blur(self, intensity):
        self.img = self.model.get_current()
        self.img = self.model.blur(self.img, intensity)
        self.ok()

    # Apply canny edge detection to dummy image
    def canny_edges(self):
        self.img = self.model.canny_edges(self.img)
        self.ok()

    # Apply brightness to dummy image
    def brightness(self, beta):
        self.img = self.model.get_current()
        self.img = self.model.brightness(self.img, beta)
        self.ok()

    # Apply contrast to dummy image
    def contrast(self, alpha):
        self.img = self.model.get_current()
        self.img = self.model.contrast(self.img, alpha)
        self.ok()

    # Rotate dummy image
    def rotate(self, angle):
        self.img = self.model.rotate(self.img, angle)
        self.ok()

    # Flip to dummy image horizontally or vertically
    def flip(self, mode):
        self.img = self.model.flip(self.img, mode)
        self.ok()

    # Resize dummy image
    def resize(self, width=None, height=None):
        self.img = self.model.resize(self.img, width, height)
        self.ok()

    # Save Image
    def save(self):
        now = str(int(datetime.now().timestamp() * 1000))
        self.model.save(self.img, f"image_{now}.jpg")

    # Save Image with specific name and filetype
    def save_as(self, name):
        self.model.save(self.img, f"{name}")

    # Commit transformation
    def ok(self):
        self.model.set_current(self.img)

    # Cancel transformation
    def cancel(self):
        self.img = self.model.get_current()

    # Reset to original condition
    def reset(self):
        self.img = self.model.reset()
