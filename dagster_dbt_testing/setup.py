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
        "dagster @ git+https://github.com/dagster-io/dagster.git@al/04-10-ci_testing#subdirectory=python_modules/dagster",
        "dagster-dbt @ git+https://github.com/dagster-io/dagster.git@al/04-10-ci_testing#subdirectory=python_modules/libraries/dagster-dbt",
        "dagster-cloud @ git+https://github.com/dagster-io/dagster-cloud.git@al/04-10-ci-test#subdirectory=dagster-cloud",
        "dagster-cloud-cli @ git+https://github.com/dagster-io/dagster-cloud.git@al/04-10-ci-test#subdirectory=dagster-cloud-cli",
        "dbt-duckdb",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ],
    },
)
