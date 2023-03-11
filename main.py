from dotenv import load_dotenv

load_dotenv()

import asyncio
import io
import os

from PIL import Image

from client import PlaceClient
from constants import Environment


# Start a websocket
# In the initial image load, detect all changes between the target and


async def get_image(websocket):
    while True:
        data = await websocket.recv()
        if type(data) == bytes:
            return Image.open(io.BytesIO(data))


async def main():
    # Grab the image we want to setup
    width, height = int(os.getenv(Environment.CANVAS_HEIGHT)), int(os.getenv(Environment.CANVAS_HEIGHT))
    original_image = Image.open(os.getenv(Environment.SOURCE_FILE))
    original_image = original_image.resize((width, height), Image.LANCZOS)

    # Start connection and get client connection protocol
    client = await PlaceClient.connect(os.getenv(Environment.WEBSOCKET_ADDRESS))
    client.current_target = original_image
    asyncio.create_task(client.receive())

    # await asyncio.sleep(2)
    await client.complete(5)

    print('Complete.')

    return


if __name__ == "__main__":
    asyncio.run(main())
