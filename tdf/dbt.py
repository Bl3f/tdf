import os

import yaml

from dagster import DagsterInstance, SourceAsset, load_assets_from_modules

from . import assets
from .contracts import Dataset


def generate_dbt_sources(sources_file):
    groups = ["lake"]
    instance = DagsterInstance.get()
    sources = {}
    for group in groups:
        for asset in load_assets_from_modules([assets]):
            try:
                if (
                    not isinstance(asset, SourceAsset)
                    and asset.group_names_by_key
                    and len(asset.keys) == 1
                    and asset.group_names_by_key[asset.key] == group
                ):
                    contract = None
                    if (
                        hasattr(asset, "metadata_by_key")
                        and "contract" in asset.metadata_by_key[asset.key]
                    ):
                        contract: Dataset = asset.metadata_by_key[asset.key]["contract"]

                    materialization = instance.get_latest_materialization_event(
                        asset.key
                    )

                    path = None
                    if materialization and asset.partitions_def:
                        materialization = materialization.asset_materialization
                        path = os.path.join(
                            os.path.dirname(materialization.metadata["path"].path),
                            "*.parquet",
                        )
                    elif materialization:
                        materialization = materialization.asset_materialization
                        path = materialization.metadata["path"].path

                    source_name = asset.node_def.name

                    if not sources:
                        sources = {"name": group, "tables": []}

                    external_location = (
                        {"external_location": path.replace("gcs", "s3")} if path else {}
                    )
                    source = {
                        "name": source_name,
                        "description": contract.description if contract else "",
                        "columns": contract.get_dbt_serialization() if contract else [],
                        "meta": {"dagster": {"asset_key": source_name}}
                        | external_location,
                    }
                    sources["tables"].append(source)
            except Exception as er:
                raise er
                pass

        with open(sources_file, "w") as f:
            f.write("version: 2\n\n")
            yaml.dump({"sources": [sources]}, f, sort_keys=False)
