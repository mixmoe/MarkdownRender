import asyncio
import os
from enum import Enum
from io import BytesIO
from pathlib import Path
from secrets import token_urlsafe

import imgkit
import markdown2


class SupportStyles(str, Enum):
    air = "air"
    modest = "modest"
    retro = "retro"
    splendor = "splendor"
    standard = "standard"


class TempFile:
    def __init__(self, ext: str = ".tmp", dir: Path = Path(".")):
        self.dir = dir / (token_urlsafe(24) + ext)

    def __enter__(self) -> Path:
        return self.dir

    def __exit__(self, *args):
        if not self.dir.exists():
            return
        os.remove(self.dir)


def _rend(body: str, style: SupportStyles = SupportStyles.standard):
    html = markdown2.markdown(body)
    with TempFile(ext=".jpg") as file:
        imgkit.from_string(
            html,
            output_path=str(file.absolute()),
            options={"encoding": "utf-8"},
            css=[f"styles/{style.value}.css"],
        )
        content: bytes = file.read_bytes()
    return content


async def render(
    content: str, style: SupportStyles = SupportStyles.standard, timeout: float = 6
) -> BytesIO:
    response = await asyncio.wait_for(
        asyncio.get_running_loop().run_in_executor(None, lambda: _rend(content, style)),
        timeout,
    )
    return BytesIO(response)
