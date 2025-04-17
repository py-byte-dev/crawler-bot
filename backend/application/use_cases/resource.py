import asyncio
from collections.abc import Collection
from concurrent.futures import ProcessPoolExecutor
from decimal import ROUND_HALF_UP, Decimal
from functools import partial

from backend.application import interfaces
from backend.application.dto.resource import ProcessedResourceDTO
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
        self._file_donloader = file_downloader
        self._xlsx_reader = xlsx_reader
        self._http_client = http_client
        self._page_content_parser = page_content_parser
        self._uuid_generator = uuid_generator

    async def __call__(self, message: interfaces.Message) -> Collection[ProcessedResourceDTO]:
        file_obj = await self._file_donloader.download(message=message)
        resources_dto = self._xlsx_reader.read(file_obj=file_obj.file_obj)

        tasks = [self._http_client.get_page_content(url=resourse.url) for resourse in resources_dto]
        pages_content = await asyncio.gather(*tasks)

        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(
                self._process_pool,
                partial(self._page_content_parser.parse, content=content, xpath=resourse.xpath),
            )
            for resourse, content in zip(resources_dto, pages_content, strict=False)
        ]

        resource_prices = await asyncio.gather(*tasks)

        processed_resources = []

        for resourse, prices in zip(resources_dto, resource_prices, strict=False):
            if prices:
                averege_price = sum(Decimal(price) for price in prices) / Decimal(len(prices))
                averege_price = averege_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                averege_price = None

            processed_resources.append(
                ProcessedResourceDTO(
                    title=resourse.title,
                    url=resourse.url,
                    xpath=resourse.xpath,
                    averege_price=averege_price,
                ),
            )

        resources_dm = [
            ResourceDM(
                id=self._uuid_generator(),
                title=resourse.title,
                url=resourse.url,
                xpath=resourse.xpath,
            )
            for resourse in resources_dto
        ]

        await self._saver.save(resources=resources_dm)
        await self._db_session.commit()

        return processed_resources
