from typing import Any

from aws_cdk import Stack
from aws_cdk import Stage
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct

from api.infrastructure import API
from database.infrastructure import Database


class UserManagementBackend(Stage):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        database_dynamodb_billing_mode: dynamodb.BillingMode,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        stateful = Stack(self, "Stateful")
        database = Database(
            stateful, "Database", dynamodb_billing_mode=database_dynamodb_billing_mode
        )
        stateless = Stack(self, "Stateless")
        api = API(
            stateless,
            "API",
            dynamodb_table=database.table,
        )
        print(api)
