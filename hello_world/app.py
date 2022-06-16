# Author: Tim Pugh
# References:
# Why You Should Never, Ever print() in a Lambda Function - https://towardsdatascience.com/why-you-should-never-ever-print-in-a-lambda-function-f997d684a705
# Instrumenting Python code in AWS Lambda - https://docs.aws.amazon.com/lambda/latest/dg/python-tracing.html and its updated source code https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/blank-python/function/lambda_function.py
# AWS X-Ray SDK for Python - https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-python.html
import os
import sys
import json
import boto3
import logging
import traceback
import jsonpickle
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

# example of building clients above/outside the Lambda handler
#client = boto3.client('lambda')
# client.get_account_settings()


def lambda_handler(event, context):
    try:
        logger.info(f'## ENVIRONMENT VARIABLES\r' +
                    jsonpickle.encode(dict(**os.environ)))
        logger.info(f'## EVENT\r' + jsonpickle.encode(event))
        logger.info(f'## CONTEXT\r' + jsonpickle.encode(context))
        
        #Create a simple error to test error logging
        #a = 2/0
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "hello world",
                }
            ),
        }

    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(
            exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)
