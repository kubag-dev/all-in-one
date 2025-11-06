from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from core.database import get_session
from todos import types
from todos.exceptions import InstanceAlreadyExistsError
from todos.exceptions import InstanceNotFoundError
from todos.exceptions import UniqueConstraintViolatedError
from todos.models.todo_file import TodoFile
from todos.schemas.todo_file_update_schema import TodoFileUpdateSchema


class TodoFileRepository:
    """
    Module is too small and basic to force returns of separate DTOs
    on pydantic's BaseModel
    """

    def __init__(self):
        self.session = get_session()

    def fetch_active_todo_files(self):
        active_todo_files = self.session.exec(
            select(TodoFile).where(TodoFile.is_deleted == False)
        ).all()
        return active_todo_files

    def fetch_inactive_todo_files(self):
        inactive_todo_files = self.session.exec(
            select(TodoFile).where(TodoFile.is_deleted == True)
        ).all()
        return inactive_todo_files

    def fetch_todo_file(self, *, todo_file_id: types.TodoFileId) -> TodoFile:
        todo_file = self.session.get(TodoFile, todo_file_id)
        if not todo_file:
            raise InstanceNotFoundError(f"Todo file not found.")
        return todo_file

    def create_todo_file(self, *, todo_file: TodoFile) -> TodoFile:
        new_todo_file = TodoFile(**todo_file.model_dump())

        try:
            self.session.add(new_todo_file)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise InstanceAlreadyExistsError("Todo file already exists.")

        self.session.refresh(new_todo_file)
        return new_todo_file

    def update_todo_file(
        self, *, todo_file_id: types.TodoTaskId, todo_file_data: TodoFileUpdateSchema
    ) -> TodoFile:
        todo_file = self.session.get(TodoFile, todo_file_id)
        if not todo_file:
            raise InstanceNotFoundError("Todo file not found")

        update_data = todo_file_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo_file, key, value)

        try:
            self.session.add(todo_file)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise UniqueConstraintViolatedError(
                f"Unique constraint violated: {e}",
            )

        self.session.refresh(todo_file)
        return todo_file

    def delete_todo_file(self, *, todo_file_id: types.TodoFileId) -> None:
        todo_file = self.session.get(TodoFile, todo_file_id)
        if not todo_file:
            raise InstanceNotFoundError("Todo file not found")

        if todo_file.is_deleted:
            self.session.delete(todo_file)
            self.session.commit()
            return None
        else:
            todo_file.is_deleted = True
            self.session.add(todo_file)
            self.session.commit()

        return None
