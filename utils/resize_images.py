import os
from PIL import Image
from django.conf import settings


def resize_image(img_name, new_width):
    img_path = os.path.join(settings.MEDIA_ROOT, img_name)
    img = Image.open(img_path)
    width, height = img.size
    new_height = round((new_width * height) / width)

    if width <= new_width:
        img.close()
        return

    new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    new_img.save(
        img_path,
        optimize=True,
        quality=80
    )
    new_img.close()
