from aiohttp import ClientSession

from backend.application import interfaces


class HttpClient(interfaces.HttpClient):
    def __init__(
        self,
        session: ClientSession,
    ):
        self._session = session

    async def get_page_content(self, url: str) -> str | None:
        async with self._session.get(url) as response:
            if response.status != 200:
                return None
            return await response.text()
