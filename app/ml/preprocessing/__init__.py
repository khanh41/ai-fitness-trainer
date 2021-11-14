import tensorflow as tf

from app.ml.base_model.movenet import input_size


def preprocessing_image_movenet(image):
    input_image = tf.expand_dims(image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)
    return input_image
