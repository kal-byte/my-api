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

import utils
import polaroid
from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse


router = APIRouter()


@utils.to_thread
def generate_image(image: bytes) -> BytesIO:
    """The backend code that generates the inverted effect for the image."""
    image = polaroid.Image(image)
    image.invert()

    buffer = BytesIO(image.save_bytes())
    return buffer


@router.get("/invert")
async def serve_image(image: str):
    resp = await utils.get_image(image)

    if isinstance(resp, JSONResponse):
        return resp

    image = await generate_image(resp)
    return StreamingResponse(image, media_type="image/png")
