import os
from typing import List

from PIL import Image

from constants import Environment
from pixel_types import Pixel


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
            if cur_pixel != target_pixel:
                results.append((x, y, target_pixel))

    return results
