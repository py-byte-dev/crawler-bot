from io import BytesIO

from backend.application import interfaces
from backend.domain.entities.document_dm import DocumentDM
from backend.infrastructrure import exceptions as infrastructure_exc


class FileDownloader(interfaces.FileDownloader):
    async def download(self, message: interfaces.Message) -> DocumentDM:
        file_id = self._get_file_metadata(message)
        file = await message.bot.get_file(file_id=file_id)
        file_path = file.file_path
        file_obj = BytesIO()
        await message.bot.download_file(file_path=file_path, destination=file_obj)
        file_obj.seek(0)

        return DocumentDM(
            file_obj=file_obj,
        )

    @staticmethod
    def _get_file_metadata(message: interfaces.Message) -> str:
        content_type = message.content_type
        if content_type == 'document':
            if 'xls' not in message.document.file_name:
                raise infrastructure_exc.IncorrectDocumentExtensionError
            return message.document.file_id
        raise infrastructure_exc.IncorrectContentTypeError(content_type=content_type)
