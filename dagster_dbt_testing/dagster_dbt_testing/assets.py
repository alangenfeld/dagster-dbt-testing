from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from .project import dagster_dbt_testing_project


@dbt_assets(manifest=dagster_dbt_testing_project.manifest_path)
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    context.log.info(f"defer args: {dbt.get_defer_args()}")
    yield from dbt.cli(["build"], context=context).stream()
