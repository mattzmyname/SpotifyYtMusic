import pathlib

from aws_cdk import (aws_dynamodb as dynamodb, aws_iam as iam)
from constructs import Construct


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        dynamodb_table: dynamodb.Table,
        lambda_reserved_concurrency: int,
    ):
        super().__init__(scope, id_)

        service_principal = iam.ServicePrincipal("lambda.amazonaws.com")
        # This policy is used for writing to Amazon CloudWatch Logs
        policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            "service-role/AWSLambdaBasicExecutionRole"
        )
        handler_role = iam.Role(
            self,
            "HandlerRole",
            assumed_by=service_principal,
            managed_policies=[policy],
        )

        dynamodb_table.grant_read_write_data(handler_role)
