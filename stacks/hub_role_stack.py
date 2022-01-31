from aws_cdk import (
	aws_iam as iam,
)
import aws_cdk as cdk
from constructs import Construct
from .config import ORG_ACCOUNT

class HubRoleStack(cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		org_read_role = 'arn:aws:iam::' + ORG_ACCOUNT + ':role/security/org-read-only-001' 
		cloudtrail_lake_read_role = 'arn:aws:iam::' + ORG_ACCOUNT + ':role/security/cloudtrail-lake-read-role'
		
		hub_role_policy = iam.ManagedPolicy(self, 'hub-001-policy',
			managed_policy_name='hub-001-policy',
			description='Policy for Automation',
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
				sid="AssumeRoleInTarget",
				effect=iam.Effect.ALLOW,
				actions=["sts:AssumeRole"],
				resources=["arn:aws:iam::*:role/security/spoke-001", org_read_role, cloudtrail_lake_read_role],
				conditions={
				"Bool": {
				  "aws:SecureTransport": "true"
					}
			  	}
				)
			]			
		)

		dynamodb_role_policy = iam.ManagedPolicy(self, 'dynamodb-hub-policy',
			managed_policy_name='dynamodb-001-policy',
			description='Policy for DynamoDB access',
			statements=[
				iam.PolicyStatement(
					sid="DynamoDBAccess",
					actions=[
						"dynamodb:GetItem",
						"dynamodb:PutItem"
					],
				effect=iam.Effect.ALLOW,
				resources=['*']
				)
			] 

		
		)		

		hub_role = iam.Role(
			self, 'hub-001',
			role_name='hub-001',
			assumed_by=iam.CompositePrincipal(
				iam.ServicePrincipal('lambda.amazonaws.com'),
				iam.ServicePrincipal('ec2.amazonaws.com')
				),
			path='/security/'
		)

		hub_role_policy.attach_to_role(hub_role)
		dynamodb_role_policy.attach_to_role(hub_role)
		hub_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonAPIGatewayInvokeFullAccess'))
		hub_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole'))
		hub_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaRole'))