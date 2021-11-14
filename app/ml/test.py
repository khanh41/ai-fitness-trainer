import time

import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt

from app.ml.base_model.movenet import movenet, input_size
from app.ml.data_loader import load_image
from app.ml.figures.draw_keypoints import draw_prediction_on_image

now = time.time()
image = load_image("C:\\Users\\tranv\Downloads\\huong-dan-chong-day-dung-cach-cho-nguoi-moi-tap-Push-Up.jpg")
# Resize and pad the image to keep the aspect ratio and fit the expected size.
input_image = tf.expand_dims(image, axis=0)
input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

# Run model inference.
keypoints_with_scores = movenet(input_image)
print(time.time() - now)

# Calculate the angle between the three landmarks.
# angle = calculateAngle((558, 326, 0), (642, 333, 0), (718, 321, 0))
# Display the calculated angle.
# print(f'The calculated angle is {angle}')

# Visualize the predictions with image.
display_image = tf.expand_dims(image, axis=0)
display_image = tf.cast(tf.image.resize_with_pad(display_image, 1280, 1280), dtype=tf.int32)
output_overlay = draw_prediction_on_image(np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

plt.figure(figsize=(5, 5))
plt.imshow(output_overlay)
_ = plt.axis('off')
plt.show()
