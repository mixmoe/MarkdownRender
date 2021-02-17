import asyncio
from enum import Enum
from io import BytesIO

import imgkit
import markdown2

from .config import Settings


class SupportStyles(str, Enum):
    air = "air"
    modest = "modest"
    retro = "retro"
    splendor = "splendor"
    standard = "standard"


def _rend(body: str, style: SupportStyles = SupportStyles.standard):
    html = markdown2.markdown(body)
    content = imgkit.from_string(
        html,
        output_path=False,
        options=Settings.options,
        css=[f"styles/{style.value}.css"],
    )
    assert isinstance(content, bytes)
    return BytesIO(content)


async def render(
    content: str,
    style: SupportStyles = SupportStyles.standard,
    timeout: float = Settings.timeout,
) -> BytesIO:
    response = await asyncio.wait_for(
        asyncio.get_running_loop().run_in_executor(None, lambda: _rend(content, style)),
        timeout,
    )
    return response
