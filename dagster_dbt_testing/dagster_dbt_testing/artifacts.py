from dataclasses import dataclass
from functools import cached_property
import os
from pathlib import Path
from typing import Optional
from dagster_dbt import DbtCliResource
import shutil


def is_cloud_branch_deployment():
    return os.getenv("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT") == "1"


def is_cloud_full_deployment():
    return "DAGSTER_CLOUD_DEPLOYMENT_NAME" in os.environ


def get_cloud_deployment_name():
    return os.environ["DAGSTER_CLOUD_DEPLOYMENT_NAME"]


@dataclass
class DagsterCloudDbtArtifacts:
    project_dir: Path
    package_data_dir: Optional[Path]

    def compile_manifest(self) -> Path:
        return (
            DbtCliResource(project_dir=os.fspath(self.project_dir))
            .cli(
                ["--quiet", "parse"],
                target_path=Path("target"),
            )
            .wait()
            .target_path.joinpath("manifest.json")
        )

    def copy_to_package_data(self) -> None:
        assert self.package_data_dir is not None
        if self.package_data_dir.exists():
            shutil.rmtree(self.package_data_dir)

        # Determine if the package data dir is within the project dir, and ignore
        # that path if so.
        rel_path = Path(os.path.relpath(self.package_data_dir, self.project_dir))
        rel_ignore = ""
        if len(rel_path.parts) > 0 and rel_path.parts[0] != "..":
            rel_ignore = rel_path.parts[0]

        shutil.copytree(
            src=self.project_dir,
            dst=self.package_data_dir,
            ignore=shutil.ignore_patterns(
                "*.git*",
                "*partial_parse.msgpack",
                rel_ignore,
            ),
        )

    def prepare_cloud_deployment(self) -> None:
        print(f"Compiling manifest.json in {self.project_dir}")
        self.compile_manifest()

        if self.package_data_dir:
            print(
                f"Copying dbt project directory {self.project_dir} to package data directory {self.package_data_dir}"
            )
            self.copy_to_package_data()

    def prepare_branch_deployment(self) -> None:
        print("Preparing dbt artifacts for branch deployment")
        self.prepare_cloud_deployment()
        #  self.download_prod_state()

    def prepare_full_deployment(self, name: str) -> None:
        print(f"Preparing dbt artifacts for {name}")
        self.prepare_cloud_deployment()
        #  self.upload_prod_state()

    def prepare_deployment(self) -> None:
        if is_cloud_branch_deployment():
            self.prepare_branch_deployment()
        elif is_cloud_full_deployment():
            name = get_cloud_deployment_name()
            self.prepare_full_deployment(name)
        else:
            raise Exception("Could not discern deployment type")

    @cached_property
    def manifest_path(self) -> Path:
        if is_cloud_branch_deployment() or is_cloud_full_deployment():
            base_dir = (
                self.package_data_dir if self.package_data_dir else self.project_dir
            )
            return base_dir / "target" / "manifest.json"
        else:
            # assume local development and live compile the manifest
            # cached_property so only once per process
            return self.compile_manifest()

    @cached_property
    def cli_resource(self) -> DbtCliResource:
        if (
            is_cloud_branch_deployment() or is_cloud_full_deployment()
        ) and self.package_data_dir:
            return DbtCliResource(project_dir=os.fspath(self.package_data_dir))

        return DbtCliResource(project_dir=os.fspath(self.project_dir))


dagster_dir = (Path(__file__) / ".." / "..").resolve()
dbt_artifacts = DagsterCloudDbtArtifacts(
    project_dir=(dagster_dir / "..").resolve(),
    package_data_dir=(dagster_dir / "dbt-project").resolve(),
)

# run this file to prepare a deployment
if __name__ == "__main__":
    dbt_artifacts.prepare_deployment()
