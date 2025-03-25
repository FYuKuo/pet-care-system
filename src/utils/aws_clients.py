from config import config
import boto3

def get_lambda_client():
    return __aws_client("lambda")

def get_s3_client():
    return __aws_client("s3")

def get_cognito_idp_client():
    return __aws_client("cognito-idp")

def get_dynamo_client():
    return __aws_resource("dynamodb")

def __aws_client(service_name: str, *, region_name: str = config.AWS_REGION):
    return boto3.client(
        service_name,
        region_name=region_name,
    )


def __aws_resource(service_name: str, *, region_name: str = config.AWS_REGION):
    return boto3.resource(
        service_name,
        region_name=region_name,
    )
