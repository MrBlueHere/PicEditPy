from pytest import fixture
from numpy.testing import assert_equal
from image_io import *
from image_operation import *


@fixture
def image():
    return read_image('tests/rick_morty.png')


@fixture
def image_sharpened():
    return read_image('tests/rick_morty_sharpened.png')


@fixture
def image_sharpened_bw():
    return read_image('tests/rick_morty_sharpened_bw.png')


@fixture
def image_bw():
    return read_image('tests/rick_morty_bw.png')


@fixture
def image_rotated():
    return read_image('tests/rick_morty_rotated.png')


@fixture
def image_flipped():
    return read_image('tests/rick_morty_flipped.png')


@fixture
def image_inverted():
    return read_image('tests/rick_morty_inverted.png')


@fixture
def images_lightened():
    return read_image('tests/rick_morty_lightened_50.png'), read_image('tests/rick_morty_lightened_100.png')


@fixture
def images_darkened():
    return read_image('tests/rick_morty_darkened_50.png'), read_image('tests/rick_morty_darkened_100.png')


@fixture
def images_blurred():
    return read_image('tests/rick_morty_blured.png')


def test_sharpen(image, image_sharpened):
    assert_equal(apply_filter(image, sharpening_kernel), image_sharpened)


def test_sharpen_bw(image_bw, image_sharpened_bw):
    assert_equal(apply_filter(image_bw, sharpening_kernel), image_sharpened_bw)


def test_bw(image, image_bw):
    assert_equal(get_bw(image), image_bw)


def test_rotate(image, image_rotated):
    assert_equal(rotate(image), image_rotated)


def test_rotate_multiple(image):
    tmp = image
    for i in range(4):
        tmp = rotate(tmp)
    assert_equal(image, tmp)


def test_mirror(image, image_flipped):
    assert_equal(flip(image), image_flipped)


def test_inverse(image, image_inverted):
    assert_equal(inverse(image), image_inverted)


def test_lighten(image, images_lightened):
    assert_equal(adjust_gamma(image, 50), images_lightened[0])
    assert_equal(adjust_gamma(image, 100), images_lightened[1])


def test_darken(image, images_darkened):
    assert_equal(adjust_gamma(image, -50), images_darkened[0])
    assert_equal(adjust_gamma(image, -100), images_darkened[1])


def test_blur(image, images_blurred):
    assert_equal(apply_filter(image, approx_gaussian_blur_3_kernel), images_blurred)
