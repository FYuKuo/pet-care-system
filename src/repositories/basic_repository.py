from exceptions.custom_exceptions import DBConditionalCheckFailedException, DBException
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from utils import aws_clients
from decimal import Decimal
import json


class BasicRepository:
    def __init__(self, table_name: str):
        dynamo_client = aws_clients.get_dynamo_client()
        self.table = dynamo_client.Table(table_name)

    def get_item(self, key: dict) -> dict:

        response = self.table.get_item(Key=key)

        return response

    def create_item(self, item: dict, *, condition_expression: str = None):

        item = self._serialize_item(item)
        kwargs = {
            "Item": item,
            **(
                {"ConditionExpression": condition_expression}
                if condition_expression
                else {}
            ),
        }

        try:
            response = self.table.put_item(**kwargs)
        except ClientError as e:
            self._handle_client_error(e)

        return response

    def update_item(
        self,
        key: dict,
        update_expression: str,
        expression_value,
        *,
        expression_attribute_names: dict = None,
        condition_expression: str = None,
    ) -> dict:

        expression_value = self._serialize_item(expression_value)
        kwargs = {
            "Key": key,
            "UpdateExpression": update_expression,
            "ReturnValues": "ALL_NEW",
            "ReturnConsumedCapacity": "NONE",
            "ExpressionAttributeValues": expression_value,
            **(
                {"ExpressionAttributeNames": expression_attribute_names}
                if expression_attribute_names
                else {}
            ),
            **(
                {"ConditionExpression": condition_expression}
                if condition_expression
                else {}
            ),
        }
        try:
            response = self.table.update_item(**kwargs)
        except ClientError as e:
            self._handle_client_error(e)

        return response

    def delete_item(
        self,
        key: dict,
        *,
        condition_expression: str = None,
        expression_attribute_values: dict = None,
    ):

        kwargs = {
            "Key": key,
            "ReturnValues": "ALL_OLD",
            **(
                {"ConditionExpression": condition_expression}
                if condition_expression
                else {}
            ),
            **(
                {"ExpressionAttributeValues": expression_attribute_values}
                if expression_attribute_values
                else {}
            ),
        }
        try:
            response = self.table.delete_item(**kwargs)
        except ClientError as e:
            self._handle_client_error(e)

        return response

    def query_items(
        self,
        key_conditions_expression: Key,
        *,
        filter_expression: Attr = None,
        index_name: str = None,
        limit: int = None,
        exclusive_start_key: dict = None,
    ) -> dict:

        kwargs = {
            "KeyConditionExpression": key_conditions_expression,
            **({"FilterExpression": filter_expression} if filter_expression else {}),
            **({"IndexName": index_name} if index_name else {}),
            **({"Limit": limit} if limit else {}),
            **({"ExclusiveStartKey": exclusive_start_key} if exclusive_start_key else {}),
        }

        try:
            response = self.table.query(**kwargs)
        except ClientError as e:
            self._handle_client_error(e)

        return response

    def batch_delete(self, items_to_delete: list[dict]):
        with self.table.batch_writer() as batch:
            for item in items_to_delete:
                batch.delete_item(Key=item)

    def batch_save(self, items_to_create: list[dict]):
        with self.table.batch_writer() as batch:
            for item in items_to_create:
                item = self._serialize_item(item)
                batch.put_item(Item=item)

    def _serialize_item(self, item: dict) -> dict:
        return json.loads(json.dumps(item), parse_float=Decimal)

    def _handle_client_error(self, error: ClientError):
        error_info = error.response["Error"]
        code = error_info["Code"]
        message = error_info["Message"]
        print(f"[ERROR] DynamoDB operation failed: {code}, {message}")

        if code == "ConditionalCheckFailedException":
            raise DBConditionalCheckFailedException()
        else:
            raise DBException()
