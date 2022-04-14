from aws_cdk import App

import constants
from deployment import UserManagementBackend
from pipeline import Pipeline

app = App()

# Development
UserManagementBackend(
    app,
    f"{constants.CDK_APP_NAME}-Dev",
    env=constants.DEV_ENV,
    database_dynamodb_billing_mode=constants.DEV_DATABASE_DYNAMODB_BILLING_MODE,
)

# Production pipeline
Pipeline(app, f"{constants.CDK_APP_NAME}-Pipeline", env=constants.PIPELINE_ENV)

app.synth()
