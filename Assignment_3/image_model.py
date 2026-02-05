import cv2


"""
Model layer of MVC

Owns image data - original and current
Owns undo/redo history
performs all image processing operations
handles load and save
"""


class ImageModel:
    def __init__(self):
        self.original = None
        self.current = None
        self.path = None
        self.undo_stack = []
        self.redo_stack = []

    # load an image and reset any history
    def open(self, path):
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Could not open image from: {path}")
        self.original = img.copy()
        self.current = img.copy()
        self.undo_stack = []
        self.redo_stack = []
        self.path = path

    # Return basic information about image
    def get_details(self):
        if self.current is None:
            return
        height, width = self.current.shape[:2]
        return f"height: {height}px\n" f"width: {width}\n" f"path: {self.path}"

    # Return a copy of current image
    def get_current(self):
        if self.current is None:
            return
        return self.current.copy()

    # Update the current image and update undo history and clean redo
    def set_current(self, img):
        if img is None or self.current is None:
            return
        self.undo_stack.append(self.current.copy())
        self.current = img.copy()
        self.redo_stack = []

    # Update the current image with previous image and update the redo stack
    def undo(self):
        if self.current is None:
            return
        if self.undo_stack == []:
            return self.current.copy()
        prev = self.current.copy()
        self.current = self.undo_stack.pop()
        self.redo_stack.append(prev)
        return self.current.copy()

    # Update the current image with undone image and update the undo stack
    def redo(self):
        if self.current is None:
            return
        if self.redo_stack == []:
            return self.current.copy()
        prev = self.current.copy()
        self.current = self.redo_stack.pop()
        self.undo_stack.append(prev)
        return self.current.copy()

    # Save current commited image
    def save(self, img, path):
        if img is None:
            raise ValueError(f"No image open")
        is_saved = cv2.imwrite(path, img)
        if not is_saved:
            raise ValueError(f"Could not save image to: {path}")

    # Apply grayscale
    def grayscale(self, img):
        if img is None:
            raise ValueError(f"No image open")
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    def blur(self, img, intensity):
        if img is None:
            raise ValueError(f"No image open")
        if intensity <= 0:
            return img.copy()

        if intensity % 2 == 0:
            intensity += 1
        return cv2.GaussianBlur(img, (intensity, intensity), 0)

    # Apply Canny Edge Detection
    def canny_edges(self, img):
        if img is None:
            raise ValueError(f"No image open")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)

    # Apply brightness
    def brightness(self, img, beta):
        if img is None:
            raise ValueError(f"No image open")
        if beta < -100:
            beta = -100
        if beta > 100:
            beta = 100
        return cv2.convertScaleAbs(img, alpha=1, beta=beta)

    # Apply contrast
    def contrast(self, img, alpha):
        if img is None:
            raise ValueError(f"No image open")
        if alpha < 0.5:
            alpha = 0.5
        if alpha > 3.0:
            alpha = 3.0
        return cv2.convertScaleAbs(img, alpha=alpha, beta=0)

    # Apply rotation at fixed points
    def rotate(self, img, angle):
        if img is None:
            raise ValueError(f"No image open")
        if angle == 90:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180:
            return cv2.rotate(img, cv2.ROTATE_180)
        if angle == 270:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        raise ValueError("Angle must be 90, 180, or 270.")

    # Apply flip
    def flip(self, img, mode):
        if img is None:
            raise ValueError(f"No image open")
        if mode == 1:
            return cv2.flip(img, 1)
        if mode == 0:
            return cv2.flip(img, 0)
        raise ValueError("Mode must be 1 or 0")

    # Resize image
    def resize(self, img, width=None, height=None):
        if img is None:
            raise ValueError(f"No image open")
        if width is not None and not isinstance(width, int):
            raise ValueError("Width is not a whole number")
        if height is not None and not isinstance(height, int):
            raise ValueError("Height is not a whole number")

        img_height, img_width = img.shape[:2]
        if height is not None and width is not None:
            print("here")
            return cv2.resize(img, (width, height))
        if height is None and width is not None:
            print("here 2")
            return cv2.resize(img, (width, img_height))
        if height is not None and width is None:
            print("here 3")
            return cv2.resize(img, (img_width, height))
        return img.copy()

    # Return original image
    def reset(self):
        if self.original is None:
            raise ValueError(f"No image open")
        self.undo_stack.append(self.current.copy())
        self.current = self.original.copy()
        return self.current.copy()
