import logging
import boto3

codedeploy = boto3.client('codedeploy')


def pre(event, context):
    deployment_id = event['DeploymentId']
    lifecycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    logging.warning('Check some stuff before traffic has been shifted...')

    return codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
        status='Succeeded')  # status can be 'Pending'|'InProgress'|'Succeeded'|'Failed'|'Skipped'|'Unknown'


def post(event, context):
    deployment_id = event['DeploymentId']
    lifecycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    logging.warning('Check some stuff before traffic has been shifted...')

    return codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
        status='Succeeded')  # status can be 'Pending'|'InProgress'|'Succeeded'|'Failed'|'Skipped'|'Unknown'

