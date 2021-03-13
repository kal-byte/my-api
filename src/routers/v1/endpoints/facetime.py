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


@utils.in_executor
def generate_image(first_image: bytes, second_image: bytes) -> BytesIO:
    """Backend code that generates the image that provides the facetime effect."""
    img_one = polaroid.Image(first_image)
    img_two = polaroid.Image(second_image)

    img_one.resize(1024, 1024, 5)
    img_two.resize(256, 256, 5)

    facetime_btns = polaroid.Image("./static/facetimebuttons.png")
    facetime_btns.resize(1024, 1024, 5)

    img_one.watermark(img_two, 15, 15)
    img_one.watermark(facetime_btns, 0, 390)

    buffer = BytesIO(img_one.save_bytes())
    return buffer


@router.get("/facetime")
async def serve_image(first: str, second: str):
    first = await utils.get_image(first)
    second = await utils.get_image(second)

    if isinstance(first, JSONResponse):
        return first

    if isinstance(second, JSONResponse):
        return second

    image = await generate_image(first, second)
    return StreamingResponse(image, media_type="image/png")
