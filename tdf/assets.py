import pandas as pd
from dagster import DailyPartitionsDefinition, asset

from tdf.contracts import get_contract
from tdf.resources import PostgresResource

race_contract = get_contract("race")


@asset(
    partitions_def=DailyPartitionsDefinition(
        start_date="2023-07-01", end_date="2023-07-24"
    ),
    compute_kind="pandas",
    group_name="lake",
    dagster_type=race_contract.get_dagster_typing(),
)
def race(context, postgres: PostgresResource) -> pd.DataFrame:
    partition_date_str = context.asset_partition_key_for_output()

    return postgres.read(
        "race",
        columns=race_contract.get_column_names(),
        partition_column=race_contract.partition_column,
        partition_value=partition_date_str,
    )
