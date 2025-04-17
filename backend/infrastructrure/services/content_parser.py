import re
from collections.abc import Collection

from bs4 import BeautifulSoup
from lxml import etree

from backend.application import interfaces

NUMBER_PATTERN = re.compile(r'\d+(?:\.\d+)?')


class PageContentParser(interfaces.PageContentParser):
    def parse(self, content: str | None, xpath: str) -> Collection[str]:
        prices = []

        if content is None:
            return prices

        soup = BeautifulSoup(content, 'lxml')
        dom = etree.HTML(str(soup))

        for el in dom.xpath(xpath):
            text = el if isinstance(el, str) else getattr(el, 'text', str(el))
            cleaned = text.replace(' ', '').replace('\xa0', '').replace(',', '.')
            matches = re.findall(pattern=NUMBER_PATTERN, string=cleaned)

            prices.extend(matches)

        return prices
