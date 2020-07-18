import numpy as np


sharpening_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
])

approx_gaussian_blur_3_kernel = (1 / 16) * np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1],
])


# Rotate an image
def rotate(image: np.array) -> np.array:
    return np.rot90(image, -1)


# Get flipped image (mirror)
def flip(image: np.array) -> np.array:
    return np.fliplr(image)


# Transform the image to black and white
def get_bw(image: np.array) -> np.array:
    if image.ndim == 2:
        return image
    return np.average(image.astype(np.float), weights=[0.299, 0.587, 0.114], axis=2).astype(np.uint8)


# Invert colors in the image
def inverse(image: np.array) -> np.array:
    return 255 - image


# Lighten or darken the image
def adjust_gamma(image: np.array, value) -> np.array:
    to_adjust = 255 * (value / 100)
    image = np.int16(image) + to_adjust
    return np.uint8(np.clip(image, 0, 255))


# Applies some kernel on the image
def apply_filter(image: np.array, kernel: np.array) -> np.array:
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    # Flip both rows and columns of the kernel
    flipped_kernel = np.flip(kernel)

    # Add padding to the image
    padding = flipped_kernel.shape[1] // 2  # padding on each side, assuming height == width
    padded_image = add_padding(image, padding)

    if image.ndim == 2:
        return apply_grayscale_filter(padded_image, flipped_kernel, image.shape)
    else:
        return apply_rgb_filter(padded_image, flipped_kernel, image.shape)


# Adds padding to the image so that kernel can be safely applied on the edges
def add_padding(image: np.array, padding) -> np.array:
    sh = image.shape
    if image.ndim == 2:
        padded_img = np.zeros((sh[0] + (2 * padding), sh[1] + (2 * padding)), dtype=np.uint8)
        # Write content to the padded image
        padded_img[padding:(padding + sh[0]), padding:(padding + sh[1])] = image
        return padded_img

    if image.ndim == 3:
        padded_img = np.zeros((sh[0] + (2 * padding), sh[1] + (2 * padding), sh[2]), dtype=np.uint8)
        # Write content to the padded image
        padded_img[padding:(padding + sh[0]), padding:(padding + sh[1]), :] = image
        return padded_img


# Filtering for grayscale images
def apply_grayscale_filter(image: np.array, kernel: np.array, orig_shape) -> np.array:
    # We assume the height == width
    kernel_len = kernel.shape[0]

    result = [[np.sum(image[row:(row + kernel_len), col:(col + kernel_len)] * kernel)
               for col in range(orig_shape[1])] for row in range(orig_shape[0])]
    return np.uint8(np.clip(result, 0, 255))


# Filtering for RGB images, using 3 channels
def apply_rgb_filter(image: np.array, kernel: np.array, orig_shape) -> np.array:
    # We assume the height == width
    kernel_len = kernel.shape[0]

    result = [[[np.sum(image[row:(row + kernel_len), col:(col + kernel_len), channel] * kernel)
                for channel in range(orig_shape[2])] for col in range(orig_shape[1])] for row in range(orig_shape[0])]
    return np.uint8(np.clip(result, 0, 255))
