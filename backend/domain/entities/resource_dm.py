from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class ResourceDM:
    id: UUID
    title: str
    url: str
    xpath: str
