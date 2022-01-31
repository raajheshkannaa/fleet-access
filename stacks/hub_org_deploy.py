import aws_cdk as cdk
from constructs import Construct
from .hub_role_stack import HubRoleStack
from .org_read_only_role_stack import OrgReadOnlyRoleStack
from .cloudtrail_lake_read_role_stack import CloudTrailLakeReadRoleStack
from .config import HUB_ACCOUNT, ORG_ACCOUNT


org_account_env = {	'account': ORG_ACCOUNT, 'region': 'us-east-1'}
hub_account_env = {	'account': HUB_ACCOUNT, 'region': 'us-east-1'}

import boto3
from collections import OrderedDict

class HubandOrgRolePipelineStage(cdk.Stage):
	def __init__(self, scope: Construct, id: str, **kwargs):
		super().__init__(scope, id, **kwargs)

		stack1 = HubRoleStack(self, 'HubRole-Stack', env=hub_account_env)
		stack2 = OrgReadOnlyRoleStack(self, 'OrgReadOnlyRole-Stack', env=org_account_env)
		stack3 = CloudTrailLakeReadRoleStack(self, 'CloudTrailLakeReadRole-Stack', env=org_account_env)	

		stack2.add_dependency(stack1)


