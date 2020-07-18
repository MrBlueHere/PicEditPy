from PIL import Image
import numpy as np


def read_image(file_name: str) -> np.array:
    return np.asarray(Image.open(file_name), dtype=np.uint8)


def image_from_array(array, mode):
    return Image.fromarray(array, mode=mode)


def save_image(array, file_path, mode='RGB'):
    image_from_array(array, mode=mode).save(file_path)
