import base64
import io

import numpy as np
from PIL import Image


def pillow_convert_base64(image):
    image = Image.fromarray(image.astype(np.uint8))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = str(img_str)[2:-1]
    return img_str
