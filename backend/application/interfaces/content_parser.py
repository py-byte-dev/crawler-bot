from abc import abstractmethod
from collections.abc import Collection
from typing import Protocol


class PageContentParser(Protocol):
    @abstractmethod
    def parse(self, content: str | None, xpath: str) -> Collection[str]: ...
