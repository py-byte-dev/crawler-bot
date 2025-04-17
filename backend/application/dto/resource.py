from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class ResourceDTO:
    title: str
    url: str
    xpath: str


@dataclass(slots=True)
class ProcessedResourceDTO(ResourceDTO):
    averege_price: Decimal
