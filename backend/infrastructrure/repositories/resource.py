from collections.abc import Collection

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application import interfaces
from backend.domain.entities.resource_dm import ResourceDM
from backend.infrastructrure.models.resource import Resource


class ResourceRepository(interfaces.ResourceSaver):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(self, resources: Collection[ResourceDM]) -> None:
        values = [
            {
                'uuid': resourse.id,
                'title': resourse.title,
                'url': resourse.url,
                'xpath': resourse.xpath,
            }
            for resourse in resources
        ]

        stmt = insert(Resource).values(values)
        await self._session.execute(stmt)
