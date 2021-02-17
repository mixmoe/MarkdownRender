from fastapi import FastAPI, Request
from fastapi.param_functions import Body, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from httpx import AsyncClient
from pydantic import HttpUrl

from .render import SupportStyles, render

app = FastAPI(title="MarkdownRender")


@app.get("/api")
async def url_handler(content: HttpUrl, style: SupportStyles = SupportStyles.standard):
    async with AsyncClient() as client:
        response = await client.get(content)
        response.raise_for_status()
    return StreamingResponse(
        content=await render(response.text, style), media_type="image/jpeg"
    )


@app.post("/api")
async def form_handler(
    content: bytes = File(...), style: SupportStyles = Form(SupportStyles.standard)
):
    return StreamingResponse(
        content=await render(content.decode(), style), media_type="image/jpeg"
    )


@app.put("/api")
async def body_handler(
    content: str = Body(...), style: SupportStyles = Body(SupportStyles.standard)
):
    return StreamingResponse(
        content=await render(content, style), media_type="image/jpeg"
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"detail": f"{exc.__class__.__qualname__ }({exc})"}, status_code=500
    )
