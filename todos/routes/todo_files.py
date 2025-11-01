from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlite3 import IntegrityError
from sqlmodel import select
from sqlmodel import Session

from core.database import get_session
from todos.models.todo_file import TodoFile
from todos.schemas.todo_file_update_schema import TodoFileUpdateSchema
from todos import types


router = APIRouter(prefix="/todo")


@router.get("/", response_model=list[TodoFile])
def get_active_todo_files(session: Session = Depends(get_session)):
    return session.exec(select(TodoFile).where(TodoFile.is_deleted == False)).all()


@router.get("/trash", response_model=list[TodoFile])
def get_active_todo_files(session: Session = Depends(get_session)):
    return session.exec(select(TodoFile).where(TodoFile.is_deleted == True)).all()


@router.get("/{todo_file_id}", response_model=TodoFile)
def get_todo_file(
    todo_file_id: types.TodoFileId, session: Session = Depends(get_session)
):
    todo_file = session.get(TodoFile, todo_file_id)
    if not todo_file:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo File not found"
        )
    return todo_file


@router.post("/", response_model=TodoFile)
def create_todo_file(todo_file: TodoFile, session: Session = Depends(get_session)):
    new_todo_file = TodoFile(**todo_file.model_dump())
    session.add(new_todo_file)
    session.commit()
    session.refresh(new_todo_file)
    return new_todo_file


@router.patch("/{todo_file_id}", response_model=TodoFile)
def update_todo_file(
    todo_file_id: types.TodoFileId,
    todo_file_data: TodoFileUpdateSchema,
    session: Session = Depends(get_session),
):
    todo_file = session.get(TodoFile, todo_file_id)
    if not todo_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo file not found"
        )

    update_data = todo_file_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_file, key, value)

    try:
        session.add(todo_file)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Uniqe constraint violated: {e}",
        )

    session.refresh(todo_file)
    return todo_file


@router.delete("/{todo_file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_file(
    todo_file_id: types.TodoFileId, session: Session = Depends(get_session)
):
    todo_file = session.get(TodoFile, todo_file_id)
    if not todo_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo file not found"
        )

    if todo_file.is_deleted:
        session.delete(todo_file)
        session.commit()
        return None
    else:
        todo_file.is_deleted = True
        session.add(todo_file)
        session.commit()
