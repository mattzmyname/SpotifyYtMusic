# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

from aws_cdk import Environment
from aws_cdk import aws_dynamodb as dynamodb

CDK_APP_NAME = "UserManagementBackend"
CDK_APP_PYTHON_VERSION = "3.9"

# pylint: disable=line-too-long
GITHUB_CONNECTION_ARN = "arn:aws:codestar-connections:us-west-2:980290784846:connection/f8d5c1b4-9c39-4a31-b86f-2fd576481134"
GITHUB_OWNER = "mattzmyname"
GITHUB_REPO = "SpotifyYtMusic"
GITHUB_TRUNK_BRANCH = "main"

DEV_ENV = Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)
DEV_API_LAMBDA_RESERVED_CONCURRENCY = 1
DEV_DATABASE_DYNAMODB_BILLING_MODE = dynamodb.BillingMode.PAY_PER_REQUEST

PIPELINE_ENV = Environment(account="980290784846", region="us-west-2")

PROD_ENV = Environment(account="980290784846", region="us-west-2")
PROD_DATABASE_DYNAMODB_BILLING_MODE = dynamodb.BillingMode.PROVISIONED
