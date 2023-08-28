from typing import Any, Mapping, Optional

from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets

from dagster import OpExecutionContext
from tdf.resources import dbt_manifest_path


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        return "warehouse"


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def analytics_dbt_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
