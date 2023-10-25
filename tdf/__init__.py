from dagster import Definitions, EnvVar, load_assets_from_modules

from . import assets
from .io_manager import GCSParquetIOManager
from .resources import GCSResource, GoogleSheetResource, PostgresResource
from .resources import dbt as dbtResource

all_assets = load_assets_from_modules([assets])

gcs = GCSResource(
    project="blef-data-platform",
    service_account_json=EnvVar("SERVICE_ACCOUNT_BASE64"),
)


defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": GCSParquetIOManager(
            base_path=EnvVar("GCS_BUCKET"),
            gcs=gcs,
        ),
        "postgres": PostgresResource(
            uri=EnvVar("POSTGRES_URI"),
        ),
        "sheets": GoogleSheetResource(),
        "dbt": dbtResource,
    },
)
