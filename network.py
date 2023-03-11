from typing import Generator, Any, List, Tuple

from multiping import multi_ping

from pixel_types import Pixel

# The largest possible chunk that can be given to Multiping
maximum_chunk = (2 ** 16) - 1


def get_ip(x: int, y: int, rgb: Tuple[int, int, int], large: bool = False):
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

    chunked = list(chunkify(ips, min(maximum_chunk, chunk_size)))
    for i, chunk in enumerate(chunked, start=1):
        print(f'Chunk {i}/{len(chunked)}')
        multi_ping(chunk, timeout=0.2, retry=0)
