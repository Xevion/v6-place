from typing import Generator, Any, List, Tuple

from multiping import multi_ping
from progressbar import progressbar
from place.pixel_types import Pixel

# The largest possible chunk that can be given to Multiping
maximum_chunk = (2 ** 16) - 1


def get_ip(x: int, y: int, rgb: Tuple[int, int, int], large: bool = False):
    """
    Build the destination IP address given the constants. Arguments are not tested for validity.

    :param x: The X coordinate as an integer. [0, 512]
    :param y: The Y coordinate as an integer. [0, 512]
    :param rgb: The RGB of each pixel described by a tuple of integers. [0, 255]
    :param large: If true, will place 2x2 pixels instead. Defaults to False.
    :return: The IPv6 address as a string.
    """
    return f"2a06:a003:d040:{'2' if large else '1'}{x:03X}:{y:03X}:{rgb[0]:02X}:{rgb[1]:02X}:{rgb[2]:02X}"


def chunkify(sequence: List[Any], size: int) -> Generator[List[Any], None, None]:
    """
    :param sequence: The sequence of items.
    :param size: The size of each individual chunk, at largest.
    :return: A generator of lists, each chunk no larger than `size`.
    """
    size = max(1, size)
    return (sequence[i:i + size] for i in range(0, len(sequence), size))


def upload_pixels(pixels: List[Pixel], chunk_size: int = None):
    """
    Given a list of pixels, upload them with the given chunk size.
    """
    ips = [get_ip(x, y, rgb) for x, y, rgb in pixels]
    return upload(ips, chunk_size)


def upload(ips: List[str], chunk_size: int = None):
    # Default to maximum chunk size
    if chunk_size is None: chunk_size = maximum_chunk

    # random.shuffle(ips)
    chunked = list(chunkify(ips, min(maximum_chunk, chunk_size)))
    for i, chunk in progressbar(list(enumerate(chunked, start=1))):
        multi_ping(chunk, timeout=0.1, retry=0)
