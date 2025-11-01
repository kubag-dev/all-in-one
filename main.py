from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.database import create_db_and_tables
from home.routes import root_route
from todos.routes import todo_files
from todos.routes import todo_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(root_route.router)
app.include_router(todo_files.router)
app.include_router(todo_tasks.router)
