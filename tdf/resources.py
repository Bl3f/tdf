from typing import List, Optional

import pandas as pd
from dagster import ConfigurableResource
from sqlalchemy import create_engine


class PostgresResource(ConfigurableResource):
    uri: str

    def read(
        self,
        table: str,
        columns: Optional[List[str]] = [],
        partition_column: Optional[str] = None,
        partition_value: Optional[str] = None,
    ):
        engine = create_engine(self.uri, echo=False)
        sql = f"""
            SELECT {','.join(columns) if columns else '*'}
            FROM {table}
            WHERE {partition_column} = '{partition_value}'
        """
        return pd.read_sql(sql, con=engine)
