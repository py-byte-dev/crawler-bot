from collections.abc import AsyncIterable, Iterable
from concurrent.futures import ProcessPoolExecutor

from aiohttp import ClientSession
from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.application import interfaces
from backend.config import Config
from backend.infrastructrure.repositories.resource import ResourceRepository
from backend.infrastructrure.services.content_parser import PageContentParser
from backend.infrastructrure.services.file_downloader import FileDownloader
from backend.infrastructrure.services.http_client import HttpClient
from backend.infrastructrure.services.user_keyboard_builder import UserKeyboardBuilder
from backend.infrastructrure.services.xlsx_reader import XlsxReader


class InfrastructureProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_process_pool(self) -> Iterable[ProcessPoolExecutor]:
        process_pool = ProcessPoolExecutor(max_workers=4)
        yield process_pool
        process_pool.shutdown()

    @provide(scope=Scope.REQUEST, provides=ClientSession)
    async def get_client_session(self) -> ClientSession:
        session = ClientSession()
        yield session
        await session.close()

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(
            config.db.create_connection_string(),
        )
        return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[
        AnyOf[
            AsyncSession,
            interfaces.DBSession,
        ]
    ]:
        async with session_maker() as session:
            yield session

    file_downloader = provide(
        FileDownloader,
        scope=Scope.REQUEST,
        provides=interfaces.FileDownloader,
    )

    xlsx_reader = provide(
        XlsxReader,
        scope=Scope.REQUEST,
        provides=interfaces.XlsxReader,
    )

    user_keyboard_builder = provide(
        UserKeyboardBuilder,
        scope=Scope.REQUEST,
        provides=interfaces.UserKeyboardBuilder,
    )

    page_content_parser = provide(
        PageContentParser,
        scope=Scope.REQUEST,
        provides=interfaces.PageContentParser,
    )

    http_client = provide(
        HttpClient,
        scope=Scope.REQUEST,
        provides=interfaces.HttpClient,
    )

    resource_repo = provide(
        ResourceRepository,
        scope=Scope.REQUEST,
        provides=interfaces.ResourceSaver,
    )
