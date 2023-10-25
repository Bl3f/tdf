import json
from typing import Any, Mapping, Optional

from dagster_dbt import DagsterDbtTranslator, dbt_assets

from dagster import OpExecutionContext
from tdf.resources import DbtResource, dbt_manifest_path


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        return "warehouse"


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def analytics_dbt_assets(context: OpExecutionContext, dbt: DbtResource):
    macro_args = {"vars": "ext_full_refresh: true"}
    yield from dbt.cli(["run-operation", "stage_external_sources", "--vars", "ext_full_refresh: true"], manifest=dbt_manifest_path).stream()
    yield from dbt.build(context)
