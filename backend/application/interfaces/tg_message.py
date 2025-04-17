from abc import abstractmethod
from typing import BinaryIO, Protocol


class Document(Protocol):
    file_id: str
    file_name: str


class File(Protocol):
    file_id: str
    file_unique_id: str
    file_size: int | None
    file_path: str | None


class Bot(Protocol):
    @abstractmethod
    async def get_file(self, file_id: str) -> File: ...

    @abstractmethod
    async def download_file(self, file_path: str, destination: BinaryIO) -> BinaryIO: ...


class Message(Protocol):
    bot: Bot
    message_id: int
    content_type: str
    document: Document | None
