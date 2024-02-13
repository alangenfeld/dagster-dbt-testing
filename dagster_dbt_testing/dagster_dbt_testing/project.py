from dagster_dbt import DbtProject
from pathlib import Path

dagster_dbt_testing_project = DbtProject(
    project_dir=Path(__file__).parent.parent.parent,
    packaged_project_dir=Path(__file__).parent.joinpath("dbt-project"),
    state_path=Path("target/managed_state"),
)
