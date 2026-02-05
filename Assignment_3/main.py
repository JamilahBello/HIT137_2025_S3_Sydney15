from image_model import ImageModel
from image_controller import ImageController
from image_view import ImageView


def main():
    model = ImageModel()
    controller = ImageController(model)
    view = ImageView(controller)
    view.run()


if __name__ == "__main__":
    main()
