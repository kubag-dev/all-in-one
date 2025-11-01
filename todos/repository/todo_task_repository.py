from fastapi import Depends
from sqlmodel import select
from sqlmodel import Session

from core.database import get_session
from todos.models.todo_task import TodoTask
from todos import types


class TodoTaskRepository:
    def assign_new_position(
        todo_task_id: types.TodoTaskId,
        new_position: int,
        session: Session = Depends(get_session),
    ) -> None:
        """
        MOVE LOGIC TO LOGIC
        """
        pointed_task = session.get(TodoTask, todo_task_id)
        tasks = session.exec(
            select(TodoTask).where(TodoTask.todo_file_id == pointed_task.todo_file_id)
        ).all()
        if new_position > pointed_task.position:
            tasks_to_reposition = [
                task
                for task in tasks
                if task.position <= new_position
                and task.position > pointed_task.position
            ]
            for task in tasks_to_reposition:
                task.position = task.position - 1
        elif new_position < pointed_task.position:
            tasks_to_reposition = [
                task
                for task in tasks
                if task.position >= new_position
                and task.position < pointed_task.position
            ]
            for task in tasks_to_reposition:
                task.position = task.position + 1
        else:
            return None

        pointed_task.position = None
        session.add(pointed_task)
        session.commit()
        session.add_all(tasks_to_reposition)
        session.commit()

    def generate_new_position(
        todo_file_id: types.TodoFileId, session: Session = Depends(get_session)
    ) -> int:
        todo_tasks = session.exec(
            select(TodoTask).where(TodoTask.todo_file_id == todo_file_id)
        ).all()
        return max([todo_task.position for todo_task in todo_tasks])

    def delete_task_and_reposition(
        todo_task_id: types.TodoTaskId, session: Session = Depends(get_session)
    ) -> None:
        pointed_task = session.get(TodoTask, todo_task_id)
        todo_tasks = session.exec(
            select(TodoTask).where(
                TodoTask.todo_file_id == pointed_task.todo_file_id,
                TodoTask.position > pointed_task.position,
            )
        ).all()
        for task in todo_tasks:
            task.position - 1
        session.delete(pointed_task)
        session.commit()
        session.add_all(todo_tasks)
        session.commit()
