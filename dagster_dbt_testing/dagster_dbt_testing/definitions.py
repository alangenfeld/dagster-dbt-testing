from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import jaffle_shop_dbt_assets
from .schedules import schedules
from .project import dagster_dbt_testing_project

defs = Definitions(
    assets=[jaffle_shop_dbt_assets],
    schedules=schedules,
    resources={"dbt": DbtCliResource(dagster_dbt_testing_project)},
)
