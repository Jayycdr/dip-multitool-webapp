from PIL import Image


def compress_image(image_path):

    image = Image.open(image_path)

    output_path = "static/uploads/compressed.png"

    image.save(output_path, optimize=True)

    return output_path