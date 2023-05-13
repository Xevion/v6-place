import os
from typing import List, Union

from PIL import Image

from place.constants import Environment
from place.pixel_types import Pixel, AlphaPixel


def is_pixel_equal(a: Union[Pixel, AlphaPixel], b: Union[Pixel, AlphaPixel]) -> bool:
    return a[0] == b[0] and a[1] == b[1] and a[2] == b[2]


def get_pixel_differences(source: Image, target: Image) -> List[Pixel]:
    """
    Returns a list of pixels (location & color) that must be changed to match `source` to `target`.

    :param source: The source image (what we currently have).
    :param target: The target image (what we want to have).
    :return: A list of pixels in tuples.
    """
    width, height = int(os.getenv(Environment.CANVAS_HEIGHT)), int(os.getenv(Environment.CANVAS_HEIGHT))
    source_pixels = source.load()
    target_pixels = target.load()
    results = []

    for y in range(width):
        for x in range(height):
            cur_pixel = source_pixels[x, y]
            target_pixel = target_pixels[x, y]
            if not is_pixel_equal(cur_pixel, target_pixel):
                results.append((x, y, target_pixel))

    return results
