from setuptools import find_packages, setup

setup(
    name="tdf",
    packages=find_packages(exclude=["tdf_tests"]),
    install_requires=[
        "dagster-webserver >= 1.4.6",
        "dagster >= 1.4.6",
        "dagster-cloud >= 1.4.6",
        "pandas >= 2.0.3",
        "psycopg2-binary >= 2.9.7",
        "dagster-pandas >= 0.20.7",
        "dagster-gcp >= 0.20.7",
        "gcsfs >= 2023.6.0",
        "dagster-dbt >= 0.20.7",
        "dbt-duckdb >= 1.6.0",
        "bdp-contracts == 0.1.2",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
