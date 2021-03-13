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

from routers import v1
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()
app.include_router(v1.router, prefix="/v1")


ref = {
    "/v1/oil": {
        "params": ["Optional: intensity - float", "Optional: radius - int"],
        "returns": "image/png"
    },
    "/v1/facetime": {
        "params": ["first_image - url", "second_image - url"],
        "returns": "image/png"
    },
    "/v1/invert": {
        "params": ["image - url"],
        "returns": "image/png"
    },
    "/v1/alwayshasbeen": {
        "params": ["text - string"],
        "returns": "image/png"
    }
}


@app.get("/", response_class=PlainTextResponse)
async def index():
    base = ""

    for key, value in ref.items():
        base += f"{key} - Params: {', '.join(value['params'])} - Returns: {value['returns']}\n"

    return base
