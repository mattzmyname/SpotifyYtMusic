import json
import pathlib
from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import pipelines
from constructs import Construct

import constants
from deployment import UserManagementBackend


class Pipeline(Stack):
    def __init__(self, scope: Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        codepipeline_source = pipelines.CodePipelineSource.connection(
            f"{constants.GITHUB_OWNER}/{constants.GITHUB_REPO}",
            constants.GITHUB_TRUNK_BRANCH,
            connection_arn=constants.GITHUB_CONNECTION_ARN,
        )
        synth_python_version = {
            "phases": {
                "install": {
                    "runtime-versions": {"python": constants.CDK_APP_PYTHON_VERSION}
                }
            }
        }
        synth_codebuild_step = pipelines.CodeBuildStep(
            "Synth",
            input=codepipeline_source,
            partial_build_spec=codebuild.BuildSpec.from_object(synth_python_version),
            install_commands=["./scripts/install-deps.sh"],
            commands=["./scripts/run-tests.sh", "npx cdk synth"],
            primary_output_directory="cdk.out",
        )
        codepipeline = pipelines.CodePipeline(
            self,
            "CodePipeline",
            cli_version=Pipeline._get_cdk_cli_version(),
            cross_account_keys=True,
            synth=synth_codebuild_step,
        )

        self._add_prod_stage(codepipeline)

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = (
            pathlib.Path(__file__).resolve().parent.joinpath("package.json")
        )
        with open(package_json_path, encoding="utf8") as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    def _add_prod_stage(self, codepipeline: pipelines.CodePipeline) -> None:
        prod_stage = UserManagementBackend(
            self,
            f"{constants.CDK_APP_NAME}-Prod",
            env=constants.PROD_ENV,
            database_dynamodb_billing_mode=constants.PROD_DATABASE_DYNAMODB_BILLING_MODE,
        )
        api_endpoint_url_env_var = f"{constants.CDK_APP_NAME.upper()}_API_ENDPOINT_URL"
        smoke_test_commands = [f"echo ${api_endpoint_url_env_var}"]
        smoke_test_shell_step = pipelines.ShellStep(
            "SmokeTest",
            commands=smoke_test_commands,
        )
        codepipeline.add_stage(prod_stage, post=[smoke_test_shell_step])
