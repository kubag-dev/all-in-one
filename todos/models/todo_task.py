import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel
from sqlmodel import UniqueConstraint

if TYPE_CHECKING:
    from todos.models.todo_file import TodoFile


class TodoTask(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("todo_file_id", "position"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    text: str = Field()
    is_completed: bool = Field(default=False)
    position: int | None = Field()

    todo_file_id: uuid.UUID = Field(
        foreign_key="todofile.id", nullable=False, ondelete="CASCADE"
    )
    todo_file: "TodoFile" = Relationship(back_populates="todo_tasks")
