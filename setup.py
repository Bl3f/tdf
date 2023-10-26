from setuptools import find_packages, setup

setup(
    name="tdf",
    packages=find_packages(exclude=["tdf_tests"]),
    install_requires=[
        "dagster-webserver == 1.4.7",
        "dagster == 1.4.7",
        "dagster-cloud == 1.4.7",
        "pandas >= 2.0.3",
        "psycopg2-binary >= 2.9.7",
        "dagster-pandas == 0.20.7",
        "dagster-gcp == 0.20.7",
        "gcsfs >= 2023.6.0",
        "dagster-dbt == 0.20.7",
        "dbt-core == 1.6.0",
        "dbt-duckdb == 1.6.1",
        "duckdb == 0.9.1",
        "bdp-contracts == 0.1.3",
        "dbt-bigquery == 1.6.7",
        "s3fs == 2023.10.0",
        "pandas-gbq == 0.19.2",
        "driftdb == 0.0.1-alpha.9",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
