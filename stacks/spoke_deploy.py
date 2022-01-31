import aws_cdk as cdk
from constructs import Construct
import boto3
from time import sleep

from .spoke_role_stack import SpokeRoleStack
from .config import ORG_ACCOUNT

def get_org_accounts(session):
	org_client = session.client('organizations')

	results = []
	messages = []
	paginator = org_client.get_paginator('list_accounts')
	response_iterator = paginator.paginate()

	for response in response_iterator:
		results = results + response['Accounts']

	for index in results:
		messages = messages + (index['Id']).split()
		
	messages.remove(ORG_ACCOUNT) # We will not deploy the Spoke Role in the Organization Account.

	return messages


class SpokeRolePipelineStage(cdk.Stage):
	def __init__(self, scope: Construct, id: str, **kwargs):
		super().__init__(scope, id, **kwargs)

		accounts = get_org_accounts(boto3.Session())

		for account in accounts:
			env = { 'account': account, 'region': 'us-east-1' } # Builds the environment variables account and region which will be used to determine which account the stack will be deployed to
			stack_name = 'SpokeRole-Stack-' + account # This needs to be unique as the stack name is not reusable for different environments.
			
			SpokeRoleStack(self, stack_name, env=env) # Invoke the actual stack with the corresponding environment variable to deploy into the specific account.
