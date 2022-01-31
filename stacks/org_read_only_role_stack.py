from aws_cdk import (
	aws_iam as iam,
)

from stacks.config import HUB_ACCOUNT
import aws_cdk as cdk
from constructs import Construct
class OrgReadOnlyRoleStack(cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)
		
		org_read_only_role_policy = iam.ManagedPolicy(self, 'org-read-only-001-policy',
			managed_policy_name='org-read-only-001-policy',
			description='Org Read Only Policy for Automation',
			statements = [
			iam.PolicyStatement(
			sid="BasicIamInfoGathering",
			actions=["sts:GetCallerIdentity",
				"iam:GetUser",
				"iam:ListRoles",
				"iam:ListAccountAliases"],
			effect=iam.Effect.ALLOW,
			resources=['*'],
			),
			iam.PolicyStatement(
				sid="OrgReadOnly",
				effect=iam.Effect.ALLOW,
				actions=[
					"organizations:Describe*",
					"organizations:List*"
				],
				resources=['*'],
				conditions={
					"Bool": {
						"aws:SecureTransport": "true"
					}
				}
			)
			]			
		)

		assume_arn_principal = 'arn:aws:iam::' + HUB_ACCOUNT + ':role/security/hub-001' # This could easily be a wildcard and no necessary to hardcode this. However for the sake of security :P we make sure only this account can assume the Org Read Only Role
		
		org_read_only_role = iam.Role(
			self, 'org-read-only-001',
			role_name='org-read-only-001',
			description='Org Read Only role to gather Organization Account Information for automation purposes',
			assumed_by=iam.CompositePrincipal(
				iam.ServicePrincipal('lambda.amazonaws.com'),
				iam.ServicePrincipal('ec2.amazonaws.com'),
				iam.ArnPrincipal(assume_arn_principal)
				),
			path='/security/'
		)

		org_read_only_role_policy.attach_to_role(org_read_only_role)
