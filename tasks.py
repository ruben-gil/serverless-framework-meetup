import os
import json
import logging
import uuid

import boto3


def get_table(environ):

    if environ == 'local':
        return boto3.resource('dynamodb', endpoint_url='http://localhost:4569')

    return boto3.resource('dynamodb')
        

def create_task(event, context):

    dynamodb = get_table(os.environ['STAGE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TASKS_TABLE'])

    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the task item.")

    item = {
        'id': str(uuid.uuid1()),
        'text': data['text'],
        'checked': False
    }

    # write the task to the database
    table.put_item(
        Item = item
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }
    return response


def get_task(event, context):

    dynamodb = get_table(os.environ['STAGE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TASKS_TABLE'])

    # fetch task from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response


def list_tasks(event, context):

    dynamodb = get_table(os.environ['STAGE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TASKS_TABLE'])

    # fetch all tasks from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response


def update_task(event, context):

    dynamodb = get_table(os.environ['STAGE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TASKS_TABLE'])

    data = json.loads(event['body'])

    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the task item.")

    # update the task in the database
    result = table.update_item(
        Key = {
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames = {
          '#task_text': 'text',
        },
        ExpressionAttributeValues = {
          ':text': data['text'],
          ':checked': data['checked']
        },
        UpdateExpression = 'SET #task_text = :text, '
                           'checked = :checked, ',
        ReturnValues = 'ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }

    return response


def delete_task(event, context):

    dynamodb = get_table(os.environ['STAGE'])
    table = dynamodb.Table(os.environ['DYNAMODB_TASKS_TABLE'])

    # delete the task from the database
    table.delete_item(
        Key = {
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
