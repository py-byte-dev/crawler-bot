from backend.infrastructrure.exceptions.base import BaseInfrastructureError


class IncorrectContentTypeError(BaseInfrastructureError):
    def __init__(self, content_type: str):
        super().__init__(f'Content type: {content_type} not supported')


class IncorrectDocumentExtensionError(BaseInfrastructureError):
    def __init__(self):
        super().__init__('Supported only .xlsx extension')
