from PIL import Image


def encode_text(image_path, message):

    image = Image.open(image_path)
    encoded = image.copy()

    width, height = image.size
    index = 0

    message += "###END###"

    for row in range(height):
        for col in range(width):

            if index < len(message):

                pixel = list(image.getpixel((col, row)))

                pixel[0] = ord(message[index])

                encoded.putpixel((col, row), tuple(pixel))

                index += 1

    output_path = "static/uploads/encoded.png"

    encoded.save(output_path)

    return output_path


def decode_text(image_path):

    image = Image.open(image_path)

    width, height = image.size

    message = ""

    for row in range(height):
        for col in range(width):

            pixel = image.getpixel((col, row))

            char = chr(pixel[0])

            message += char

            if message.endswith("###END###"):
                return message[:-9]

    return "No hidden message found"