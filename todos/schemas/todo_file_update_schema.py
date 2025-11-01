from sqlmodel import SQLModel


class TodoFileUpdateSchema(SQLModel):
    title: str | None = None
    description: str | None = None
    is_deleted: bool | None = None
