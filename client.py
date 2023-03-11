import asyncio
import io
import os
from typing import Optional, List, Union

import websockets
from PIL import Image

from constants import Environment
from differencing import get_pixel_differences
from network import upload_pixels
from pixel_types import Pixel

width, height = int(os.getenv(Environment.CANVAS_HEIGHT)), int(os.getenv(Environment.CANVAS_HEIGHT))
total_pixels = width * height
minimum_tolerance = 5 / total_pixels


class PlaceClient:
    """
    Defines a stateful client that manages a 'source of truth' with the image created by incremental changes to the Websocket.
    """

    def __init__(self, connection) -> None:
        self.connection: websockets.WebSocketClientProtocol = connection

        # A lock used to manage the 'source of truth' image while performing read intensive operations.
        self.source_lock = asyncio.Lock()

        # The 'source of truth' image describing what is currently on the canvas.
        self.source: Image = Image.new("RGBA", (width, height), (255, 0, 0, 0))

        # The current targeted 'output' image.
        self.current_target: Optional[Image] = None

    def lock(self) -> asyncio.Lock:
        return self.source_lock

    async def get_differences(self) -> List[Pixel]:
        """
        :return: A list of pixels that must be placed on the canvas to meet the currently set task.
        """
        if self.current_target is not None:
            async with self.lock():
                return get_pixel_differences(self.source, self.current_target)
        return []

    async def complete(self, tolerance: Union[int, float] = 15, sleep: float = 0.25) -> None:
        pixel_tolerance = tolerance if type(tolerance) == int else total_pixels * tolerance

        if self.current_target is None:
            return

        pixels = await self.get_differences()
        while len(pixels) > pixel_tolerance:
            # Upload all the differences
            upload_pixels(pixels)

            # Wait a bit for the client to catch up. Is this super necessary?
            await asyncio.sleep(sleep)

            # Recalculate the difference
            pixels = await self.get_differences()

    @classmethod
    async def connect(cls, address: str):
        """A factory method for connecting to the websocket and instantiating the client."""
        connection = await websockets.connect(address)
        client = cls(connection)
        if connection.open:
            message = await connection.recv()
            if type(message) != bytes:
                raise RuntimeError("Fatal: Initial message from websocket was not 'bytes'")

            img = Image.open(io.BytesIO(message))
            client.source.paste(img)

        return client

    async def receive(self):
        """
            Receiving all server messages and handling them
        """
        while True:
            try:
                message = await self.connection.recv()
                if type(message) == bytes:
                    img = Image.open(io.BytesIO(message))

                    async with self.lock():
                        self.source.paste(img, (0, 0), img)

            except websockets.ConnectionClosed:
                print('Connection with server closed')
                break
