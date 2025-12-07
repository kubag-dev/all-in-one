from datetime import datetime
import uuid

from sqlalchemy.dialects.sqlite import JSON
from sqlmodel import Column
from sqlmodel import Field
from sqlmodel import SQLModel

from notifications import types


class DateNotification(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    reminder_at: datetime = Field()
    is_read: bool = Field(default=False)

    attached_to_module: types.Modules = Field(index=True)
    attached_to_item_types: types.ModuleItemTypesMap = Field(sa_column=Column(JSON))
    attached_to_item: uuid.UUID | str = Field(index=True)
