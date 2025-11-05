from typing import Any

from sqlmodel import delete
from sqlmodel import select
from sqlmodel import update

from core.database import get_session
from todos.models.todo_file import TodoFile
from todos.models.todo_task import TodoTask
from todos import types


class TodoTaskRepository:
    """
    Module is too small and basic to force returns of separate DTOs
    on pydantic's BaseModel
    """

    def __init__(self):
        self.session = get_session()

    def fetch_all_tasks(self, *, todo_file_id: types.TodoFileId) -> list[TodoTask]:
        return self.session.exec(
            select(TodoTask).where(TodoTask.todo_file_id == todo_file_id)
        ).all()

    def create_task(
        self, *, todo_file_id: types.TodoFileId, todo_task: TodoTask
    ) -> TodoTask:
        parent = self.session.get(TodoFile, todo_file_id)
        if not parent:
            raise Exception("Parent not found")

        new_todo_task = TodoTask(**todo_task.model_dump(), todo_file_id=todo_file_id)

        self.session.add(new_todo_task)
        self.session.commit()
        self.session.refresh(new_todo_task)
        return new_todo_task

    def update_task(
        self, *, todo_task_id: types.TodoTaskId, todo_update_data: dict[str, Any]
    ):
        todo_task = self.session.get(TodoTask, todo_task_id)
        if not todo_task:
            raise Exception("Todo task not found")

        for key, value in todo_update_data.items():
            setattr(todo_task, key, value)

        self.session.add(todo_task)
        self.session.commit()
        self.session.refresh(todo_task)
        return todo_task

    def assign_new_position(
        self,
        *,
        todo_task_id: types.TodoTaskId,
        new_position: int,
    ) -> None:
        current_position, todo_file_id = self.session.exec(
            select(TodoTask.position, TodoTask.todo_file_id).where(
                TodoTask.id == todo_task_id
            )
        ).first()
        if current_position == new_position:
            return None

        self.session.exec(update(TodoTask).where(TodoTask.todo_file_id == todo_task_id).values(position=None))  # type: ignore
        self.session.commit()

        if new_position > current_position:
            self.session.exec(
                update(TodoTask)
                .where(
                    (TodoTask.todo_file_id == todo_file_id)
                    & (TodoTask.position <= new_position)
                    & (TodoTask.position > current_position)
                )
                .values({TodoTask.position: TodoTask.position - 1})
            )
        elif new_position < current_position:
            self.session.exec(
                update(TodoTask)
                .where(
                    (TodoTask.todo_file_id == todo_file_id)
                    & (TodoTask.position >= new_position)
                    & (TodoTask.position < current_position)
                )
                .values({TodoTask.position: TodoTask.position + 1})
            )

        self.session.exec(update(TodoTask).where(TodoTask.todo_file_id == todo_task_id).values(position=new_position))  # type: ignore
        self.session.commit()
        return None

    def generate_new_position(
        self,
        *,
        todo_file_id: types.TodoFileId,
    ) -> int:
        todo_tasks_positions = self.session.exec(
            select(TodoTask.position).where(TodoTask.todo_file_id == todo_file_id)
        ).all()
        if not todo_tasks_positions:
            return 0
        return int(max(todo_tasks_positions))

    def delete_task_and_reposition(self, *, todo_task_id: types.TodoTaskId) -> None:
        current_position, todo_file_id = self.session.exec(
            select(TodoTask.position, TodoTask.todo_file_id).where(
                TodoTask.id == todo_task_id
            )
        ).first()

        if not todo_file_id:
            raise Exception("Todo file not found")

        self.session.exec(delete(TodoTask).where(TodoTask.id == todo_task_id))  # type: ignore
        self.session.commit()

        self.session.exec(
            update(TodoTask)
            .where(
                TodoTask.todo_file_id == todo_file_id,
                TodoTask.position > current_position,
            )
            .values({TodoTask.position: TodoTask.position - 1})
        )
        self.session.commit()
        return None
