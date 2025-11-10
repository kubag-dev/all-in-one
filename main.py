from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.database import create_db_and_tables
from home.routes import root_route
from todos.routes import todo_files
from todos.routes import todo_tasks

from gui.todos.views import todo_file_view
from gui.home.views import home_view


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Backend routes
app.include_router(root_route.router)
app.include_router(todo_files.router)
app.include_router(todo_tasks.router)

# Frontend views
app.include_router(home_view.router)
app.include_router(todo_file_view.router)


app.mount("/gui", StaticFiles(directory="gui"), name="gui")
app.mount("/static", StaticFiles(directory="gui/static"), name="static")
