import os
from io import BytesIO

import aiohttp

AUTOTAGGER_URL = os.getenv("AUTOTAGGER_URL", "http://localhost:5000/evaluate")


async def is_tagger_alive() -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.head(AUTOTAGGER_URL) as r:
            return r.status == 200


async def tagger(image: bytes, filename="image.jpg"):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field(
            "file", BytesIO(image), filename=filename, content_type="image/jpeg"
        )
        data.add_field("format", "json")
        async with session.post(AUTOTAGGER_URL, data=data) as r:
            r.raise_for_status()
            response = await r.json()
            if (
                isinstance(response, dict)
                and response.get("error") == "UnindentifiedImageError"
            ):
                return []
            tags = []
            for name, rating in response[0]["tags"].items():
                if rating > 0.5:
                    tags.append(name)
            return tags
