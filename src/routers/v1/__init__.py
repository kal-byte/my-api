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

import pathlib
from fastapi import APIRouter


# Get the endpoints path.
path = pathlib.Path("./routers/v1/endpoints")
# Put all files that that match `*.py` and don't start with a `_`
# and removing the `.py` in a list.
end_points = [x.name[:-3] for x in path.glob("[!_]*.py")]


# Instantiate the API Router.
router = APIRouter()
for ep in end_points:
    # This block creates code (To be executed) that
    # imports the endpoint from the route folder
    # and then includes it in the router.
    block = (
        f"from routers.v1.endpoints import {ep}\n"
        f"router.include_router({ep}.router)"
    )
    # This line then executes the block.
    exec(block)
