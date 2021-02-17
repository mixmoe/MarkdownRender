import asyncio

from fastapi import FastAPI, Response
from fastapi.param_functions import Body, File, Form

from .render import rend

app = FastAPI(title="MarkdownRender")


@app.post("/")
async def render(content: bytes = File(...), style: str = Form("standard")):
    loop = asyncio.get_running_loop()
    response = await asyncio.wait_for(
        loop.run_in_executor(None, rend, content), timeout=7
    )
    return Response(content=response, media_type="image/jpeg")


@app.put("/")
async def _(content: str = Body(...), style: str = Body("standard")):
    return await render(content.encode(), style)
