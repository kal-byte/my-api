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
import textwrap
from io import BytesIO
from fastapi import APIRouter, Query
from PIL import Image, ImageFont, ImageDraw
from fastapi.responses import StreamingResponse


router = APIRouter()
default_text = "You should consider putting in some actual text."


@utils.in_executor
def generate_image(text: str) -> BytesIO:
    """Backend code that generates the image to make the "Always Has Been" meme."""
    with Image.open("./static/ahb.png") as img:
        wrapped = textwrap.wrap(text, 20)

        font = ImageFont.truetype("./static/Roboto-Medium.ttf", 36)
        draw = ImageDraw.Draw(img)

        cur_height, pad = 300, 5
        for line in wrapped:
            w, h = draw.textsize(line, font=font)
            draw.text(((img.width - w) / 2, cur_height), line, font=font)
            cur_height -= h + pad

        buffer = BytesIO()
        img.save(buffer, "png")

    buffer.seek(0)
    return buffer


@router.get("/alwayshasbeen")
async def serve_image(text: str = Query(default_text)):
    image = await generate_image(text)
    return StreamingResponse(image, media_type="image/png")
