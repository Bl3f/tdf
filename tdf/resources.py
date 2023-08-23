from typing import Optional

import pandas as pd
from dagster import ConfigurableResource
from sqlalchemy import create_engine


class PostgresResource(ConfigurableResource):
    uri: str

    def read(
        self,
        table: str,
        partition_column: Optional[str] = None,
        partition_value: Optional[str] = None,
    ):
        engine = create_engine(self.uri, echo=False)
        sql = f"""
            SELECT *
            FROM {table}
            WHERE {partition_column} = '{partition_value}'
        """
        return pd.read_sql(sql, con=engine)
