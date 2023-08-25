import os

from dagster_dbt import DbtCliResource

from dagster import Definitions, EnvVar, load_assets_from_modules

from . import assets
from .dbt import generate_dbt_sources
from .io_manager import GCSParquetIOManager
from .resources import GCSResource, GoogleSheetResource, PostgresResource

all_assets = load_assets_from_modules([assets])

gcs = GCSResource(
    project="blef-data-platform",
    service_account_json=EnvVar("SERVICE_ACCOUNT_JSON"),
)

LOCAL = "local"
if os.getenv("ENV") == LOCAL:
    generate_dbt_sources("analytics/models/generated_sources.yml")

dbt = DbtCliResource(project_dir="analytics", target=os.getenv("DBT_TARGET"))
dbt_parse_invocation = dbt.cli(["parse"], manifest={}).wait()

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
        "dbt": dbt,
    },
)
