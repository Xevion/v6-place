# v6-place

I found a neat website called [**Place: IPv6**](https://v6.sys42.net/) and found the idea really cool.

If you've ever heard of /r/place, you'll remember that you can place pixels on a globally-synchronized
canvas, creating any sort of image you want.

Instead of having a user-controllable interface or an HTTP API, this website relies on IPv6 addresses to place pixels on the canvas.

This repository is a custom "library" built to do just that - paint on the canvas.

## How does it work?

It's all Python, and I use a couple magic libraries to do most of the heavy lifting, namely:

- [`multiping`][pypi-multiping] - Allows me to send out tens of thousands of pings per second.
- Pillow - Image operations, resizing, conversions etc.
- [`websockets`][pypi-websockets] - Allows me to hook into the canvas image and detect changes
- `asyncio` - Required for use by [`websockets`][pypi-websockets], allows me to send pings & process data simultaneously.

The simple steps to this program are:
- Read the image I want the canvas to contain. Resize to 512x512 (canvas size).
- Connect to the websocket and begin reading image data.
  - This is a background process as well, and will continue to read and process changes.
  - Doing so is required as it allows me to more efficiently upload changes to the canvas.
- Find the difference between the canvas and the target image
- Upload all pixels from the target image
  - Once done, we will check the difference again and upload those pixels.

## Issues

There is one glaring flaw with this application, and most of the processing is done to fix it (indirectly)...

**Not every ping will color a pixel.**

Why? I have no earthly idea. But unfortunately, I believe it is inherent to the speed at which I dispatch ICMP Echo
requests, and lowering the speed even by 50% would be untenable, and even doing that did not resolve the issue.

So, as it stands now, the issue is solved by being efficient rather than accurate (making sure each pixel is painted correctly).
- By efficient, I mean  only targeting pixels that _need_ to be changed.

[pypi-multiping]: https://pypi.org/project/multiping/
[pypi-websockets]: https://pypi.org/project/websockets/