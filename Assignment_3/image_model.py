import cv2


class ImageModel:
    def __init__(self):
        self.original = None
        self.current = None
        self.path = None
        self.undo_stack = []
        self.redo_stack = []

    def open(self, path):
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Could not open image from: {path}")
        self.original = img.copy()
        self.current = img.copy()
        self.path = path

    def get_details(self):
        height, width = self.current.shape[:2]
        print(f"height: {height}\n width: {width}\n path: {self.path}")

    def get_current(self):
        if self.current is None:
            raise ValueError("No image open")
        return self.current.copy()

    def set_current(self, img):
        if img is None and self.current is None:
            raise ValueError("No image open")
        self.undo_stack.append(self.current.copy())
        self.current = img.copy()
        self.redo_stack = []

    def undo(self):
        if self.current is None:
            raise ValueError("No image open")
        if self.undo_stack == []:
            return self.current.copy()
        prev = self.current.copy()
        self.current = self.undo_stack.pop()
        self.redo_stack.append(prev)
        return self.current.copy()

    def redo(self):
        if self.current is None:
            raise ValueError("No image open")
        if self.redo_stack == []:
            return self.current.copy()
        prev = self.current.copy()
        self.current = self.redo_stack.pop()
        self.undo_stack.append(self.current.copy())
        return self.current.copy()

    def save(self, path):
        if self.current is None:
            raise ValueError(f"No image open")
        is_saved = cv2.imwrite(path, self.current)
        if not is_saved:
            raise ValueError(f"Could not save image to: {path}")

    def grayscale(self, img):
        if img is None:
            raise ValueError(f"No image open")
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def blur(self, img, intensity):
        if img is None:
            raise ValueError(f"No image open")
        if intensity < 1:
            intensity = 1
        if intensity % 2 == 0:
            intensity += 1
        return cv2.GaussianBlur(img, (intensity, intensity), 0)

    def canny_edges(self, img):
        if img is None:
            raise ValueError(f"No image open")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)

    def brightness(self, img, beta):
        if img is None:
            raise ValueError(f"No image open")
        if beta < -255:
            beta = -255
        if beta > 255:
            beta = 255
        return cv2.convertScaleAbs(img, alpha=1, beta=beta)

    def contrast(self, img, alpha):
        if img is None:
            raise ValueError(f"No image open")
        if alpha < -170:
            alpha = -170
        if alpha > 170:
            alpha = 170
        return cv2.convertScaleAbs(img, alpha=alpha, beta=0)

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

    def flip(self, img, mode):
        if img is None:
            raise ValueError(f"No image open")
        if mode == 1:
            return cv2.flip(img, 1)
        if mode == 0:
            return cv2.flip(img, 0)
        raise ValueError("Mode must be 1 or 0")

    def resize(self, img, width=None, height=None):
        if img is None:
            raise ValueError(f"No image open")
        if not isinstance(width, int):
            raise ValueError("Width is not a whole number")
        if not isinstance(height, int):
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
        return img

    def reset(self):
        if self.original is None:
            raise ValueError(f"No image open")
        return self.original.copy()
