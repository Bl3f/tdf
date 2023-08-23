import pandas as pd
from dagster import (
    AssetKey,
    DailyPartitionsDefinition,
    SourceAsset,
    StaticPartitionsDefinition,
    asset,
)

from tdf.contracts import get_contract
from tdf.resources import GoogleSheetResource, PostgresResource

public_race = SourceAsset(
    key=AssetKey("postgres__public_race"),
    description="A Postgres table containing race data.",
    group_name="postgres",
)

sheet = SourceAsset(
    key=AssetKey("sheet"),
    description="A Google Sheet with stages and rider informations.",
    group_name="sheet",
)

race_contract = get_contract("race")
riders_contract = get_contract("riders")
stages_info_contract = get_contract("stages_info")
stages_contract = get_contract("stages")
stages_dagster_type = stages_contract.get_dagster_typing()


@asset(
    deps=[public_race],
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
    deps=[sheet],
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
    deps=[sheet],
    compute_kind="pandas",
    dagster_type=stages_info_contract.get_dagster_typing(),
    group_name="lake",
)
def stages_info(sheets: GoogleSheetResource) -> pd.DataFrame:
    return sheets.read(
        sheet_id="1L_jMRyK77c5TRFSt__1dX6v7xWjFygIuebYQ7xY7VnY",
        sheet_name="stages_info",
    )


@asset(
    compute_kind="pandas",
    partitions_def=StaticPartitionsDefinition(
        [f"{str(i).zfill(2)}" for i in range(1, 22)]
    ),
    dagster_type=stages_dagster_type,
    group_name="local",
)
def stages_partitioned(context) -> pd.DataFrame:
    partition = context.asset_partition_key_for_output()

    df = pd.read_csv(
        f"./tdf/data/stages/{partition}.csv",
        sep=";",
        dtype={"sumcategory": str},
    )

    return df


@asset(
    compute_kind="pandas",
    dagster_type=stages_dagster_type,
    group_name="lake",
)
def stages(stages_partitioned) -> pd.DataFrame:
    return (
        pd.concat(stages_partitioned)
        .reset_index()
        .rename(columns={"level_0": "stage_id", "level_1": "index"})
    )
