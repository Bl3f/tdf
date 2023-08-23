import pandas as pd
from dagster import DailyPartitionsDefinition, asset

from tdf.contracts import get_contract
from tdf.resources import GoogleSheetResource, PostgresResource

race_contract = get_contract("race")
riders_contract = get_contract("riders")
stages_info_contract = get_contract("stages_info")


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


@asset(
    compute_kind="pandas",
    dagster_type=riders_contract.get_dagster_typing(),
    group_name="lake",
)
def riders(sheets: GoogleSheetResource) -> pd.DataFrame:
    return sheets.read(
        sheet_id="1L_jMRyK77c5TRFSt__1dX6v7xWjFygIuebYQ7xY7VnY",
        sheet_name="riders",
    )


@asset(
    compute_kind="pandas",
    dagster_type=stages_info_contract.get_dagster_typing(),
    group_name="lake",
)
def stages_info(sheets: GoogleSheetResource) -> pd.DataFrame:
    return sheets.read(
        sheet_id="1L_jMRyK77c5TRFSt__1dX6v7xWjFygIuebYQ7xY7VnY",
        sheet_name="stages_info",
    )
