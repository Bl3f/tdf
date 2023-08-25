import pandas as pd
from google.oauth2.service_account import Credentials
from upath import UPath

from dagster import (
    ConfigurableIOManagerFactory,
    InputContext,
    MetadataValue,
    OutputContext,
    UPathIOManager,
)
from tdf.resources import GCSResource


class PandasParquetIOManager(UPathIOManager):
    credentials: Credentials
    extension: str = ".parquet"

    def __init__(self, credentials, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = credentials

    def dump_to_path(self, context: OutputContext, obj: pd.DataFrame, path: UPath):
        obj.to_parquet(path, storage_options={"token": self.credentials})

        contract = context.metadata["contract"]

        context.add_output_metadata(
            {
                "preview": MetadataValue.md(obj.head().to_markdown()),
                "num_rows": len(obj),
                "schema": MetadataValue.table_schema(contract.get_schema_display()),
            }
        )

    def load_from_path(self, context: InputContext, path: UPath) -> pd.DataFrame:
        return pd.read_parquet(path, storage_options={"token": self.credentials})


class GCSParquetIOManager(ConfigurableIOManagerFactory):
    base_path: str
    gcs: GCSResource

    def create_io_manager(self, context) -> PandasParquetIOManager:
        base_path = UPath(self.base_path)
        assert str(base_path).startswith("gcs://"), base_path
        return PandasParquetIOManager(
            base_path=base_path, credentials=self.gcs.credentials
        )
