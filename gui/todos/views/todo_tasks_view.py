from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from todos import types


templates = Jinja2Templates(directory=["gui/todos/templates", "gui/templates"])
router = APIRouter(prefix="/gui/todo")


@router.get("/{todo_file_id}/tasks", response_class=HTMLResponse)
async def todo_file_view(request: Request, todo_file_id: types.TodoFileId):
    return templates.TemplateResponse(
        "todo_tasks.html", {"request": request, "todo_file_id": todo_file_id}
    )
