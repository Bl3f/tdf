from dagster import Definitions, EnvVar, load_assets_from_modules

from . import assets
from .resources import PostgresResource

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "postgres": PostgresResource(
            uri=EnvVar("POSTGRES_URI"),
        ),
    },
)
