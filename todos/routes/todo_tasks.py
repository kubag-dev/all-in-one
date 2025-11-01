from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import status
from sqlmodel import select
from sqlmodel import Session

from core.database import get_session
from todos.models.todo_file import TodoFile
from todos.models.todo_task import TodoTask
from todos.schemas.todo_task_update_schema import TodoTaskUpdateSchema
from todos import types


router = APIRouter(prefix="/todo/{todo_file_id}/tasks")


@router.get("/", response_model=list[TodoTask])
def get_todo_tasks(
    todo_file_id: types.TodoFileId = Path(...), session: Session = Depends(get_session)
):
    return session.exec(
        select(TodoTask).where(TodoTask.todo_file_id == todo_file_id)
    ).all()


@router.post("/", response_model=TodoTask)
def create_todo_task(
    todo_task: TodoTask,
    todo_file_id: types.TodoFileId = Path(...),
    session: Session = Depends(get_session),
):
    parent = session.get(TodoFile, todo_file_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Todo file not found")

    new_todo_task = TodoTask(**todo_task.model_dump(), todo_file_id=todo_file_id)

    session.add(new_todo_task)
    session.commit()
    session.refresh(new_todo_task)
    return new_todo_task


@router.patch("/{todo_task_id}", response_model=TodoTask)
def update_todo_file(
    todo_task_id: types.TodoTaskId,
    todo_file_data: TodoTaskUpdateSchema,
    session: Session = Depends(get_session),
):
    todo_task = session.get(TodoTask, todo_task_id)
    if not todo_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo task not found"
        )

    update_data = todo_file_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_task, key, value)

    session.add(todo_task)
    session.commit()
    session.refresh(todo_task)
    return todo_task


@router.delete("/{todo_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_file(
    todo_task_id: types.TodoTaskId, session: Session = Depends(get_session)
):
    todo_task = session.get(TodoTask, todo_task_id)
    if not todo_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo task not found"
        )

    session.delete(todo_task)
    session.commit()
    return None
