import os

import pandas as pd
from dagster_dbt import get_asset_key_for_model
from datagit import github_connector
from datagit.drift_evaluators import auto_merge_drift
from github import Github

from dagster import asset
from tdf.assets import analytics_dbt_assets
from tdf.resources import BigQueryResource



@asset(
    group_name="quality",
    compute_kind="datadrift",
    deps=[get_asset_key_for_model([analytics_dbt_assets], "stages_duration_per_rider")],
)
def store_metric(bigquery: BigQueryResource) -> pd.DataFrame:
    df = pd.read_gbq(
        """
        SELECT id AS unique_key, rider_slug, stage_id, date, duration 
        FROM letour.stages_duration_per_rider;
        """,
        credentials=bigquery.credentials,
    )

    github_connector.store_metric(
        dataframe=df,
        ghClient=Github(os.getenv("DATADRIFT_TOKEN")),
        filepath=f"{os.getenv('DATADRIFT_REPO')}/stages_duration_per_rider.test.csv",
        drift_evaluator=auto_merge_drift,
    )

    return df
