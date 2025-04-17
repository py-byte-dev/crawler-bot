from abc import abstractmethod
from collections.abc import Collection
from io import BytesIO
from typing import Protocol

from backend.application.dto.resource import ResourceDTO


class XlsxReader(Protocol):
    @staticmethod
    @abstractmethod
    def read(file_obj: BytesIO) -> Collection[ResourceDTO]: ...
