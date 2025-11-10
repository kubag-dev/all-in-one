from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory=["gui/home/templates", "gui/templates"])
router = APIRouter(prefix="/gui")


@router.get("/", response_class=HTMLResponse)
async def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
