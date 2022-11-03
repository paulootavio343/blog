from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


def resize_image(image, new_width):
    memory_img = BytesIO(image.read())
    img = Image.open(memory_img)
    width, height = img.size
    new_height = round((new_width * height) / width)
    img_format = os.path.splitext(image.name)[1][1:].upper()
    img_format = 'JPEG' if img_format == 'JPG' else img_format

    if width <= new_width:
        img.close()
        return image

    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(buffer, format=img_format)
    new_img = ContentFile(buffer.getvalue())
    img.close()
    return InMemoryUploadedFile(new_img, 'ImageField', image.name, img_format, None, None)
