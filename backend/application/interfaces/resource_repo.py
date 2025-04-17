from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol

from backend.domain.entities.resource_dm import ResourceDM


class ResourceSaver(Protocol):
    @abstractmethod
    async def save(self, resources: Collection[ResourceDM]) -> None: ...
