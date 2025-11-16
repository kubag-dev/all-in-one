from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import status

from todos.models.todo_task import TodoTask
from todos.repository.todo_task_repository import TodoTaskRepository
from todos.schemas.todo_task_update_schema import TodoTaskUpdateSchema
from todos import types


router = APIRouter(prefix="/todo/{todo_file_id}/tasks")


@router.get("/", response_model=list[TodoTask])
def get_todo_tasks(
    todo_file_id: types.TodoFileId = Path(...),
    todo_task_repository: TodoTaskRepository = Depends(),
):
    return todo_task_repository.fetch_all_tasks(todo_file_id=todo_file_id)


@router.post("/", response_model=TodoTask)
def create_todo_task(
    todo_task: TodoTask,
    todo_file_id: types.TodoFileId = Path(...),
    todo_task_repository: TodoTaskRepository = Depends(),
):
    try:
        task_position = todo_task_repository.generate_new_position(
            todo_file_id=todo_file_id
        )
        todo_task = todo_task_repository.create_task(
            todo_file_id=todo_file_id, todo_task=todo_task, position=task_position
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    return todo_task


@router.patch("/{todo_task_id}", response_model=TodoTask)
def update_todo_file(
    todo_task_id: types.TodoTaskId,
    todo_file_data: TodoTaskUpdateSchema,
    todo_task_repository: TodoTaskRepository = Depends(),
):
    todo_task_repository = todo_task_repository

    todo_update_data = todo_file_data.model_dump(exclude_unset=True)
    position = todo_update_data.pop("position", None)
    if position:
        todo_task_repository.assign_new_position(todo_task_id=todo_task_id, new_position=position)  # type: ignore

    try:
        todo_task = todo_task_repository.update_task(
            todo_task_id=todo_task_id, todo_update_data=todo_update_data
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo task not found"
        )

    return todo_task


@router.delete("/{todo_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_task(
    todo_task_id: types.TodoTaskId, todo_task_repository: TodoTaskRepository = Depends()
):
    todo_task_repository.delete_task_and_reposition(todo_task_id=todo_task_id)
