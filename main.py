import asyncio
import io

from PIL import Image
from websockets import connect

from differencing import get_pixel_differences
from network import upload

# Start a websocket
# In the initial image load, detect all changes between the target and

width, height = 512, 512


async def get_image(websocket):
    while True:
        data = await websocket.recv()
        if type(data) == bytes:
            return Image.open(io.BytesIO(data))


async def main():
    source_path = "C:\\Users\\Xevion\\Documents\\ShareX\\Screenshots\\2023-03\\firefox_c60J4nQj77.png"

    async with connect("wss://v6.sys42.net/ws") as websocket:
        while True:
            print(websocket.messages)

            original_image = Image.open(source_path)
            original_image = original_image.resize((width, height), Image.LANCZOS)

            source = await get_image(websocket)
            ips = get_pixel_differences(source, original_image)

            upload(ips)

            if len(ips) < 5:
                break

            original_image.close()

            break


if __name__ == "__main__":
    asyncio.run(main())
