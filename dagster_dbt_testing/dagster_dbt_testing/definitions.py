from dagster import Definitions

from .assets import jaffle_shop_dbt_assets
from .artifacts import dbt_artifacts
from .schedules import schedules

defs = Definitions(
    assets=[jaffle_shop_dbt_assets],
    schedules=schedules,
    resources={"dbt": dbt_artifacts.cli_resource},
)
