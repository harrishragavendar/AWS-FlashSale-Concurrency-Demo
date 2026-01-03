import boto3
from botocore.exceptions import ClientError
import os
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    product_id = "PRODUCT#IPHONE17"

    try:
        table.update_item(
            Key={"product_id": product_id},
            UpdateExpression="SET available_units = available_units - :one",
            ConditionExpression="available_units > :zero",
            ExpressionAttributeValues={
                ":one": 1,
                ":zero": 0
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "iPhone 17 reserved successfully"
            })
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 409,
                "body": json.dumps({
                    "message": "iPhone 17 is sold out"
                })
            }
        raise
