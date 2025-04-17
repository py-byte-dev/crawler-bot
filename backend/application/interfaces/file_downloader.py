from abc import abstractmethod
from typing import Protocol

from backend.application.interfaces.tg_message import Message
from backend.domain.entities.document_dm import DocumentDM


class FileDownloader(Protocol):
    @abstractmethod
    async def download(self, message: Message) -> DocumentDM: ...

    @staticmethod
    @abstractmethod
    def _get_file_metadata(message: Message) -> str: ...
