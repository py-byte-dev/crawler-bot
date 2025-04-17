from abc import abstractmethod
from typing import Protocol


class HttpClient(Protocol):
    @abstractmethod
    async def get_page_content(self, url: str) -> str | None: ...
