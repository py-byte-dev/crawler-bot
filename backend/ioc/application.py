from dishka import Provider, Scope, provide
from uuid6 import uuid7

from backend.application import interfaces
from backend.application.use_cases.resource import ProcessXlsxDocumentInteractor


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid7

    process_xlx_document_interactor = provide(ProcessXlsxDocumentInteractor, scope=Scope.REQUEST)
