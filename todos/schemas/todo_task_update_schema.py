from sqlmodel import SQLModel


class TodoTaskUpdateSchema(SQLModel):
    text: str | None = None
    is_complete: bool | None = None
