from typing import Dict

from pydantic import BaseSettings, Extra


class RenderSettings(BaseSettings):
    class Config:
        extra = Extra.allow

    timeout: float = 8.0
    media_type: str = "image/png"
    options: Dict[str, str] = {
        "encoding": "utf-8",
        "quiet": "",
        "disable-javascript": "",
        "zoom": "1.2",
        "load-error-handling": "ignore",
        "disable-local-file-access": "",
        "load-media-error-handling": "ignore",
        "format": "png",
    }


Settings = RenderSettings()
