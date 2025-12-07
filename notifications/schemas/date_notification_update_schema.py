from datetime import datetime

from sqlmodel import SQLModel


class DateNotificationUpdateSchema(SQLModel):
    reminder_at: datetime | None = None
    is_read: bool | None = None
