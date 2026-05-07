from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request, name="inicio.html", context={"ano_actual": datetime.now().year},
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html", context={"ano_actual": datetime.now().year},
    )


@app.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    return templates.TemplateResponse(
        request=request, name="contacto.html", context={"ano_actual": datetime.now().year},
    )
