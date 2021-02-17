"""
**A microservice that provides the function of rendering Markdown as an image.**

- API Documents:
    - [Redoc](/docs) (Easier to read and more beautiful)
    - [Swagger UI](/docs/test) (Integrated interactive testing function)

GitHub Project: https://github.com/mixmoe/MarkdownRender
"""

from fastapi import Body, FastAPI, File, Form, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from httpx import AsyncClient
from pydantic import HttpUrl

from .config import Settings
from .render import SupportStyles, render

app = FastAPI(
    title="MarkdownRender",
    description=__doc__,
    docs_url="/docs/test",
    redoc_url="/docs",
)


@app.get("/", include_in_schema=False)
async def redirect():
    return Response(status_code=302, headers={"location": "/docs"})


@app.get("/api")
async def url_handler(
    url: HttpUrl,
    style: SupportStyles = SupportStyles.standard,
):
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        content = response.text
    return StreamingResponse(
        content=await render(content, style),
        media_type=Settings.media_type,
    )


@app.post("/api")
async def form_handler(
    content: bytes = File(...),
    style: SupportStyles = Form(SupportStyles.standard),
):
    return StreamingResponse(
        content=await render(content.decode(), style),
        media_type=Settings.media_type,
    )


@app.put("/api")
async def body_handler(
    content: str = Body(...),
    style: SupportStyles = Body(SupportStyles.standard),
):
    return StreamingResponse(
        content=await render(content, style),
        media_type=Settings.media_type,
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={
            "detail": exc.__class__.__qualname__,
            "info": " ".join(str(exc).splitlines()).strip(),
        },
        status_code=500,
    )
