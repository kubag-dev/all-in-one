from enum import Enum
from typing import Literal
from typing import TypeAlias
from uuid import UUID


notificationId: TypeAlias = UUID


class Modules(str, Enum):
    TODOS = "TODOS"


ModuleItemTypesMap = dict[Modules, Literal["TASKS"]]
