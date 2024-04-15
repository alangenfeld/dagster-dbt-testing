from setuptools import find_packages, setup

setup(
    name="dagster_dbt_testing",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "dagster_dbt_testing": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt>=0.23.1",
        "dbt-duckdb",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)
