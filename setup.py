from setuptools import find_packages, setup

setup(
    name="tdf",
    packages=find_packages(exclude=["tdf_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
