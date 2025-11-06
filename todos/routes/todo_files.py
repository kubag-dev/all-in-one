from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from todos.exceptions import (
    InstanceNotFoundError,
    InstanceAlreadyExistsError,
    UniqueConstraintViolatedError,
)
from todos.models.todo_file import TodoFile
from todos.repository.todo_file_repository import TodoFileRepository
from todos.schemas.todo_file_update_schema import TodoFileUpdateSchema
from todos import types


router = APIRouter(prefix="/todo")


@router.get("/", response_model=list[TodoFile])
def get_active_todo_files():
    return TodoFileRepository().fetch_active_todo_files()


@router.get("/trash", response_model=list[TodoFile])
def get_inactive_todo_files():
    return TodoFileRepository().fetch_inactive_todo_files()


@router.get("/{todo_file_id}", response_model=TodoFile)
def get_todo_file(todo_file_id: types.TodoFileId):
    try:
        todo_file = TodoFileRepository().fetch_todo_file(todo_file_id=todo_file_id)
    except InstanceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo File not found"
        )
    return todo_file


@router.post("/", response_model=TodoFile)
def create_todo_file(todo_file: TodoFile):
    try:
        new_todo_file = TodoFileRepository().create_todo_file(todo_file=todo_file)
    except InstanceAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_todo_file


@router.patch("/{todo_file_id}", response_model=TodoFile)
def update_todo_file(
    todo_file_id: types.TodoFileId,
    todo_file_data: TodoFileUpdateSchema,
):
    try:
        todo_file = TodoFileRepository().update_todo_file(
            todo_file_id=todo_file_id, todo_file_data=todo_file_data
        )
    except InstanceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UniqueConstraintViolatedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return todo_file


@router.delete("/{todo_file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_file(todo_file_id: types.TodoFileId):
    try:
        TodoFileRepository().delete_todo_file(todo_file_id=todo_file_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
