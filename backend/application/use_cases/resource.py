import asyncio
from collections.abc import Collection
from concurrent.futures import ProcessPoolExecutor
from decimal import ROUND_HALF_UP, Decimal

from backend.application import interfaces
from backend.application.dto.resource import ProcessedResourceDTO, ResourceDTO
from backend.domain.entities.resource_dm import ResourceDM


class ProcessXlsxDocumentInteractor:
    def __init__(
        self,
        process_pool: ProcessPoolExecutor,
        db_session: interfaces.DBSession,
        saver: interfaces.ResourceSaver,
        file_downloader: interfaces.FileDownloader,
        xlsx_reader: interfaces.XlsxReader,
        http_client: interfaces.HttpClient,
        page_content_parser: interfaces.PageContentParser,
        uuid_generator: interfaces.UUIDGenerator,
    ):
        self._process_pool = process_pool
        self._db_session = db_session
        self._saver = saver
        self._downloader = file_downloader
        self._xlsx_reader = xlsx_reader
        self._http_client = http_client
        self._content_parser = page_content_parser
        self._uuid_generator = uuid_generator

    async def __call__(self, message: interfaces.Message) -> Collection[ProcessedResourceDTO]:
        xlsx_file = await self._downloader.download(message)
        resources = self._xlsx_reader.read(file_obj=xlsx_file.file_obj)

        processed = await asyncio.gather(
            *(self._fetch_and_parse(r) for r in resources),
        )

        dm_objects = [
            ResourceDM(
                id=self._uuid_generator(),
                title=r.title,
                url=r.url,
                xpath=r.xpath,
            )
            for r in resources
        ]

        await self._saver.save(resources=dm_objects)
        await self._db_session.commit()

        return processed

    async def _fetch_and_parse(self, resource: ResourceDTO) -> ProcessedResourceDTO:
        content = await self._http_client.get_page_content(url=resource.url)

        loop = asyncio.get_running_loop()
        prices = await loop.run_in_executor(
            self._process_pool,
            self._content_parser.parse,
            content,
            resource.xpath,
        )

        if prices:
            dec_prices = list(map(Decimal, prices))
            avg_price = (sum(dec_prices) / Decimal(len(dec_prices))).quantize(
                Decimal('0.01'),
                ROUND_HALF_UP,
            )
        else:
            avg_price = None

        return ProcessedResourceDTO(
            title=resource.title,
            url=resource.url,
            xpath=resource.xpath,
            average_price=avg_price,
        )
