import uuid

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from todos.models.todo_task import TodoTask


class TodoFile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str = Field(unique=True, index=True)
    description: str = Field(default="")
    is_deleted: bool = Field(default=False)

    todo_tasks: list["TodoTask"] = Relationship(
        back_populates="todo_file", cascade_delete=True
    )
