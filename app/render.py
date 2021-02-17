import os
from pathlib import Path
from secrets import token_urlsafe

import imgkit
import markdown2


class TempFile:
    def __init__(self, ext: str = ".tmp", dir: Path = Path(".")):
        self.dir = dir / (token_urlsafe(24) + ext)

    def __enter__(self) -> Path:
        return self.dir

    def __exit__(self, *args):
        if not self.dir.exists():
            return
        os.remove(self.dir)


def rend(body: str):
    html = markdown2.markdown(body)
    print(html)
    with TempFile(ext=".jpg") as file:
        imgkit.from_string(
            html,
            output_path=str(file.absolute()),
            options={"encoding": "utf-8"},
            css=["styles/modest.css"],
        )
        content: bytes = file.read_bytes()
    return content
