import click
import yaml
from bdp_contracts import Dataset, get_contracts


@click.command()
@click.argument("sources_file")
def generate_dbt_sources(sources_file):
    sources = {}
    contract: Dataset
    for contract in get_contracts().datasets:
        try:
            if not sources:
                sources = {"name": "lake", "tables": []}

            if contract.partition_column:
                external_location = f"gs://{{{{ env_var('GCS_BUCKET_NAME') }}}}/{contract.name}/*.parquet"
            else:
                external_location = f"gs://{{{{ env_var('GCS_BUCKET_NAME') }}}}/{contract.name}.parquet"

            source = {
                "name": contract.name,
                "description": contract.description,
                "columns": contract.get_dbt_serialization(with_bigquery_typing=True),
                "external": {
                    "location": external_location,
                    "options": {
                        "format": "parquet",
                    },
                },
                "meta": {
                    "dagster": {"asset_key": contract.name},
                },
            }
            sources["tables"].append(source)

        except Exception as er:
            raise er
            pass

        with open(sources_file, "w") as f:
            f.write("version: 2\n\n")
            yaml.dump({"sources": [sources]}, f, sort_keys=False)


if __name__ == "__main__":
    generate_dbt_sources()
