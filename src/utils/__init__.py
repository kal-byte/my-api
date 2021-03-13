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


async def get_image(url: str):
    """Helper method to help get an image from a URL, adds some niceties as well."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.headers["Content-Type"] not in ACCEPTED_MIME_TYPES:
                    return JSONResponse({"error": "Invalid mime type from URL."}, status_code=400)
                return await resp.read()
        except aiohttp.InvalidURL:
            return JSONResponse({"error": "Invalid URL inputted."}, status_code=400)


def in_executor(func: typing.Callable):

    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        partial = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, partial)

    return wrapper
