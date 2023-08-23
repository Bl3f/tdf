from dataclasses import dataclass, field
from typing import List, Optional

import yaml
from dagster_pandas import PandasColumn, create_dagster_pandas_dataframe_type


class ContractNotFoundError(Exception):
    def __init__(self, contract_name):
        self.contract_name = contract_name
        super().__init__(f"Contract '{self.contract_name}' not found.")


def get_pandas_column_type(name, type_, **kwargs):
    if type_ == "str":
        return PandasColumn.string_column(name, **kwargs)
    elif type_ == "int":
        return PandasColumn.integer_column(name, **kwargs)
    elif type_ == "date":
        return PandasColumn.datetime_column(name, **kwargs)
    elif type_ == "float":
        return PandasColumn.float_column(name, **kwargs)
    elif type_ == "boolean":
        return PandasColumn.boolean_column(name, **kwargs)
    else:
        raise Exception("Type not found.")


@dataclass
class Field:
    name: str
    type: str
    description: str
    options: dict = field(default_factory=dict)


@dataclass
class Dataset:
    name: str
    type: str
    description: str
    columns: List[Field]
    partition_column: Optional[str] = ""

    def __post_init__(self):
        self.columns = [Field(**column) for column in self.columns]

    def get_column_names(self):
        return [col.name for col in self.columns]

    def get_pandas_schema(self):
        return [
            get_pandas_column_type(col.name, col.type, **col.options)
            for col in self.columns
        ]

    def get_dagster_typing(self):
        return create_dagster_pandas_dataframe_type(
            name=self.name,
            columns=self.get_pandas_schema(),
        )


def get_contracts():
    with open("./tdf/contracts.yml", "r") as f:
        contracts = yaml.safe_load(f)

    return contracts


def get_contract(dataset_name):
    contracts = get_contracts()

    for contract in contracts["datasets"]:
        if contract["name"] == dataset_name:
            return Dataset(**contract)

    raise ContractNotFoundError(dataset_name)
