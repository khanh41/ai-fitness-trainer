import tensorflow as tf


# Load the input image.
def load_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image)
    return image
