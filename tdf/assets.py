import pandas as pd
from dagster import DailyPartitionsDefinition, asset

from tdf.resources import PostgresResource


@asset(
    partitions_def=DailyPartitionsDefinition(
        start_date="2023-07-01", end_date="2023-07-24"
    ),
    compute_kind="pandas",
    group_name="lake",
)
def race(context, postgres: PostgresResource) -> pd.DataFrame:
    partition_date_str = context.asset_partition_key_for_output()

    return postgres.read(
        "race",
        partition_column="updated_at",
        partition_value=partition_date_str,
    )
