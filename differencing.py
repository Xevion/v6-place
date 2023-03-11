from typing import List, Tuple
from pixel_types import RGB
from PIL import Image


def overlay_transparent(source: Image, layer: Image, differences: bool = False) -> List[Tuple[int, int]]:
    """
    Given an image, it wil be modified in-place to layer a (potentially transparent) Image on top.

    :param source: The source image to be modified.
    :param layer:  The layer to implant upon it.
    :return: If specified, a list of tuples indicating pixel locations will be returned.
    """
    return []


def get_pixel_differences(source: Image, target: Image) -> List[Tuple[int, int, RGB]]:
    """
    Returns a list of pixels (location & color) that must be changed to match `source` to `target`.

    :param source: The source image (what we currently have).
    :param target: The target image (what we want to have).
    :return: A list of pixels in tuples.
    """
    source_pixels = source.load()
    target_pixels = target.load()
    height, width = source.shape
    results = []

    for y in range(width):
        for x in range(height):
            cur_pixel = source_pixels[x, y]
            target_pixel = target_pixels[x, y]
            if cur_pixel != target_pixel:
                results.append((x, y, target_pixel))

    return results
