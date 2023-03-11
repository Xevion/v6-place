# v6-place

<div align="center">
  <a href="https://v6.sys42.net">
    <img src="https://i.xevion.dev/2023/03/firefox_UMf1xj8hrL.png" width="512"
    alt="Place IPv6 Screenshot">
      </img>
  </a>
<br />
<sub>Proof that I am talented at writing wonderfully awful software.</sub>
</div>
<br />

I found a neat website called [**Place: IPv6**](https://v6.sys42.net/) and found the idea really cool.

If you've ever heard of /r/place, you'll remember that you can place pixels on a globally-synchronized canvas, creating any sort of image you want. There is absolutely
no restriction on creativity, allowing both good and bad.

However, instead of having a user-controllable interface or an HTTP API, this website relies on IPv6 addresses to place pixels on the canvas.

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

## Usage

> This repository is highly experimental. Expect to be writing, developing & learning code inside it if you want to use it. Seriously.

I use `pipenv` for managing my virtual environments & packages. Once installed, use `pipenv install` to grab all packages & setup the environment.

Setup environment variables in `.env`:
```env
SOURCE_FILE=  # Point it to some file you want to upload. Should support most things implicitly, png, jpeg, bmp etc.
WEBSOCKET_ADDRESS=  # Grab me from IPv6 website. If you don't know how to find this, then you don't deserve to use it.
CANVAS_WIDTH=512
CANVAS_HEIGHT=512
```

Then just execute `main.py` (activate the Pipenv shell, or run `pipenv run python main.py`).

## Issues

There is one glaring flaw with this application, and most of the processing is done to fix it (indirectly)...

**Not every ping will color a pixel.**

Why? I have no earthly idea. But unfortunately, I believe it is inherent to the speed at which I dispatch ICMP Echo
requests, and lowering the speed even by 50% would be untenable, and even doing that did not resolve the issue.

So, as it stands now, the issue is solved by being efficient (only targeting pixels that _need_ to be changed.) rather than accurate (making sure each pixel is painted correctly).

## Future

This was just a small one-day project to mess around with the site, but in the case that it grabs someone's attention,
or if I really want to work on it in the future, here are some improvements to try for:
- Use numpy, CPython or some kind of compiled processing libraries to speed up the processing.
  - I have very little practice in this space, so getting some would definitely be fun to learn!
- Optimize transfers using 2x2 pixels
  - This optional is available, but is completely ignored & untested by me.
  - If implemented, this should be implemented as 'late' in the process as possible.
    - Check each pixel if all of it's neighbors (if available) are the same color.
    - If so, then remove neighbors & swap to 2x2 pixel.
- Look into alternative ways of completing the `echo`. I somehow doubt that the server is listening to complete `ICMP` packets
and verifying their authenticity - to even be able to support >10,000 pings per second without shitting the bed, it would have to be
customized, at least a little bit.
  - Look into the composition of ICMP packets, and try manually sending packets to the address until one works.
  - Once a packet is found, switch to C, look for low-level network & program optimizations, and see what the maximum "ping" rate is.
- Create various transitions
  - This is the fun idea I'm interested in. Essentially, I want to change the order of pixel placement as they are 'transferred'
  to the canvas. Instead of placing them from top to bottom, left to right or even randomly, what about a 'Radial Wipe'?
  By simply sorting the pixels by their angle to the center (with an offset, if necessary), a radial wipe effect could be achieved.
    - Pixel (16x16 blocks of pixels at a time)
    - Disc Wipe
      - Order disc by their distance from the center.
      - Optional: Group pixels by their distance, divided by 50 & rounded down. This would create a 'layering' effect.
  - Additionally, in order to deal with the effects of packet loss in regards to the animation, 'grouping' of pixels
  while completing the transfer would be interesting.
    - Instead of completing the entire layer of packets & recalculating what is next, one could process
    PART of the transition, slowly revealing parts of the image in 'layers'.
    - Each layer or group would be targeted, resolved (all pixels would be fully checked as 'written') in order.
- Add a CLI frontend
  - Currently, the entire app is controlled via environment variables & changing the code.
  This is horrible for any 'normal' user.
- Improve transparency support
  - The application doesn't handle transparency very well. Allowing the use of transparent input would be nice.
- Improve logging
  - Feedback, at least for debugging purposes, would be very helpful.
- Improve feedback
  - Progress bars, logging and in general, more feedback for the user to know what's going on would be great.
- Use asyncio properly
  - Currently, the application doesn't actually use asyncio to allow websocket handling & pinging simultaneously.
  It's better than nothing, but it could be better. A lot better.
  - Also, the application takes several more seconds than it should to exit. Why? Do I have to close the connection manually?

[pypi-multiping]: https://pypi.org/project/multiping/
[pypi-websockets]: https://pypi.org/project/websockets/