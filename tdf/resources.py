import base64
import json
from typing import List, Optional

import pandas as pd
from dagster import ConfigurableResource
from dagster_gcp import GCSResource as DagsterGCSResource
from google.cloud import storage
from google.oauth2.service_account import Credentials
from pydantic import Field
from sqlalchemy import create_engine


class PostgresResource(ConfigurableResource):
    uri: str

    def read(
        self,
        table: str,
        columns: Optional[List[str]] = [],
        partition_column: Optional[str] = None,
        partition_value: Optional[str] = None,
    ) -> pd.DataFrame:
        engine = create_engine(self.uri, echo=False)
        sql = f"""
            SELECT {','.join(columns) if columns else '*'}
            FROM {table}
            WHERE {partition_column} = '{partition_value}'
        """
        return pd.read_sql(sql, con=engine)


class GoogleSheetResource(ConfigurableResource):
    def read(self, sheet_id: str, sheet_name: str) -> pd.DataFrame:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(url)


class GCSResource(DagsterGCSResource):
    service_account_json: Optional[str] = Field(
        default=None, description="Credentials file content encoded in base64"
    )

    @property
    def credentials(self) -> Credentials:
        decoded_service_account_json = json.loads(
            base64.b64decode(self.service_account_json)
        )

        return Credentials.from_service_account_info(
            decoded_service_account_json
        ).with_scopes(["https://www.googleapis.com/auth/devstorage.read_write"])

    def get_client(self) -> storage.Client:
        return storage.client.Client(project=self.project, credentials=self.credentials)
