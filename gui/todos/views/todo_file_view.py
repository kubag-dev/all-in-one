from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory=["gui/todos/templates", "gui/templates"])
router = APIRouter(prefix="/gui/todo")


@router.get("/", response_class=HTMLResponse)
async def todo_file_view(request: Request):
    return templates.TemplateResponse("todo_file.html", {"request": request})
