import os
import unittest
from unittest.mock import patch
from tasks import *


@patch.dict(os.environ, {'STAGE': 'local', 'DYNAMODB_TASKS_TABLE': 'serverless-meetup_local_Table'}, clear=True)
@patch('tasks.boto3')
class TestMethods(unittest.TestCase):

    def test_create(self, boto3):
        event = {"body": "{ \"text\": \"hola\" }"}
        result = create_task(event, {})
        self.assertEqual(result['statusCode'], 200)

    def test_create_error(self, boto3):
        with self.assertRaises(Exception) as context:
            event = {"body": "{}"}
            result = create_task(event, {})

        self.assertTrue("Couldn't create the task item" in str(context.exception))

    def test_list(self, boto3):
        boto3.resource.return_value.Table.return_value.scan.return_value = {'Items': []}
        result = list_tasks({}, {})
        self.assertEqual(result['statusCode'], 200)

    def test_get(self, boto3):
        boto3.resource.return_value.Table.return_value.get_item.return_value = {
            'Item': {'id': '2cc2b7e6-3953-11e9-abe6-2816ad91e759'}}
        event = {'pathParameters': {'id': '2cc2b7e6-3953-11e9-abe6-2816ad91e759'}}
        result = get_task(event, {})
        self.assertEqual(result['statusCode'], 200)

    def test_update(self, boto3):
        boto3.resource.return_value.Table.return_value.update_item.return_value = {
            'Attributes': {'id': '2cc2b7e6-3953-11e9-abe6-2816ad91e759'}}
        event = {'pathParameters': {'id': '2cc2b7e6-3953-11e9-abe6-2816ad91e759'},
                 "body": "{ \"text\": \"hola\", \"checked\": \"True\" }"}
        result = update_task(event, {})
        self.assertEqual(result['statusCode'], 200)

    def test_update_error(self, boto3):
        with self.assertRaises(Exception) as context:
            event = {'pathParameters': {'id': '2cc2b7e6-3953-11e9-abe6-2816ad91e759'}, "body": "{}"}
            result = update_task(event, {})

        self.assertTrue("Couldn't update the task item" in str(context.exception))

    def test_delete(self, boto3):
        event = {'pathParameters': {'id': '1'}}
        result = delete_task(event, {})
        self.assertEqual(result['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
