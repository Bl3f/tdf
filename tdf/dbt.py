import os

import yaml

from dagster import DagsterInstance, SourceAsset, load_assets_from_modules

from . import assets


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
                        "meta": {"dagster": {"asset_key": source_name}}
                        | external_location,
                    }
                    sources["tables"].append(source)

            except Exception as er:
                pass

        with open(sources_file, "w") as f:
            f.write("version: 2\n\n")
            yaml.dump({"sources": [sources]}, f)
