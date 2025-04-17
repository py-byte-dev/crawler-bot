from collections.abc import Collection
from io import BytesIO

import pandas as pd

from backend.application import interfaces
from backend.application.dto.resource import ResourceDTO


class XlsxReader(interfaces.XlsxReader):
    @staticmethod
    def read(file_obj: BytesIO) -> Collection[ResourceDTO]:
        resources_df = pd.read_excel(file_obj, engine='openpyxl')
        return [
            ResourceDTO(
                title=row['NAME'],
                url=row['URL'],
                xpath=row['XPATH'],
            )
            for _, row in resources_df.iterrows()
        ]
