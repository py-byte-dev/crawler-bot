from dataclasses import dataclass
from io import BytesIO


@dataclass(slots=True)
class DocumentDM:
    file_obj: BytesIO
