import base64
import io
import os
import uuid

import numpy as np
from PIL import Image

from app.core.constant import ROOT_PATH


def pillow_convert_base64(image):
    image = Image.fromarray(image.astype(np.uint8))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = str(img_str)[2:-1]
    return img_str


def read_image_byte(image_byte):
    image = Image.open(io.BytesIO(image_byte))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = np.asarray(image)
    return image


def save_byte_to_video(request):
    file_path = 'app/resources/videos/' + str(uuid.uuid4()) + '.avi'
    save_path = os.path.join(ROOT_PATH, file_path)

    if os.path.isfile(save_path):
        os.remove(save_path)

    with open(save_path, "wb") as out_file:
        out_file.write(request)

    return save_path
