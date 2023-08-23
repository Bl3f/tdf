from dataclasses import dataclass, field
from typing import List, Optional

import yaml


@dataclass
class Field:
    name: str
    description: str


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


def get_contracts():
    with open("./tdf/contracts.yml", "r") as f:
        contracts = yaml.safe_load(f)

    return contracts


def get_contract(dataset_name):
    contracts = get_contracts()

    for contract in contracts["datasets"]:
        if contract["name"] == dataset_name:
            return Dataset(**contract)

    return None
