"""
MIT License

Copyright 2021-Present kal-byte

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import typing
import aiohttp
import asyncio
import functools
from fastapi.responses import JSONResponse


ACCEPTED_MIME_TYPES = ("image/jpeg", "image/png", "image/gif")


async def get_image(url: str) -> typing.Union[JSONResponse, bytes]:
    """Helper method to help get an image from a URL, adds some niceties as well."""
    # We make a new session here to be able to use it.
    # Ideally I'd want to just have one session but I'm unsure
    # how to go around this right now.
    async with aiohttp.ClientSession() as session:
        try:
            # Make the request to the URL so we can access the request body.
            async with session.get(url) as resp:
                # Here we check if the Content-Type is in the accepted mime types we have.
                # If it's not then we'll throw a JSONResponse that informs the user with a 400 status code.
                if resp.headers["Content-Type"] not in ACCEPTED_MIME_TYPES:
                    return JSONResponse({"error": "Invalid mime type from URL."}, status_code=400)
                # Return the bytes of the image since it clearly passed what we checked.
                return await resp.read()
        except aiohttp.InvalidURL:
            # If the URL is invalid then we'll throw a JSONResponse and tell the user
            # with a 400 status code.
            return JSONResponse({"error": "Invalid URL inputted."}, status_code=400)


def to_thread(func: typing.Callable) -> typing.Coroutine:

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # We make this a partial function due to readability
        # I could just pass in the function and the args & kwargs
        # to the to_thread function but this allows for easier readability.
        partial = functools.partial(func, *args, **kwargs)
        # The to_thread coroutine runs the sync function in another thread
        # and then returns the result. This achieves the same result as
        # run_in_executor for people who are on <3.9 but using this makes
        # for even more clean code.
        return await asyncio.to_thread(partial)

    return wrapper
