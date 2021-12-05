import tensorflow as tf
import tensorflow_hub as hub

from PIL import Image
from io import BytesIO

import numpy as np


# PREPARING CLASSIFIER
max_img_size = 384
classifier = hub.load('https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_s/classification/2')
warmup_input = tf.random.uniform([1, max_img_size, max_img_size, 3], 0, 1.0)
classifier(warmup_input)  # warmup


# PREPARING LABELS
with open('ImageNetLabels.txt') as f:
    labels = f.read()
    labels = labels.split('\n')
    del labels[0]
    del labels[-1]


# FUNCTIONS
def transform_image(img):
    img = Image.open(BytesIO(img))
    img = np.array(img)
    img = tf.reshape(img, [1, img.shape[0], img.shape[1], img.shape[2]])
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize_with_pad(img, max_img_size, max_img_size)
    return img


def generate_probabilities(img):
    probabilities = tf.nn.softmax(classifier(img)).numpy()
    sorted_args = tf.argsort(probabilities, axis=-1, direction='DESCENDING')[0]
    probabilities_list = []
    for arg in sorted_args:
        probabilities_list.append({
            'item': labels[arg],
            'probability': float(probabilities[0][arg])
        })
    return probabilities_list


def classify(img):
    img = transform_image(img)
    probabilities = generate_probabilities(img)
    return probabilities

