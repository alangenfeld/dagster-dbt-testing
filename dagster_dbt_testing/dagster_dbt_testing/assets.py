from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from .artifacts import dbt_artifacts


@dbt_assets(manifest=dbt_artifacts.manifest_path)
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
