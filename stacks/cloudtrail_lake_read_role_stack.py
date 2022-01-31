from aws_cdk import (
	aws_iam as iam,	
)
import aws_cdk
from constructs import Construct

from .config import HUB_ACCOUNT

class CloudTrailLakeReadRoleStack(aws_cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)
		
		cloudtrail_lake_read_role_policy = iam.ManagedPolicy(self, 'cloudtrail-lake-read-policy',
			managed_policy_name='cloudtrail-lake-read-policy',
			description='CloudTrail Lake Read Policy for Automation',
			statements = [
			iam.PolicyStatement(
				sid="CloudTrailLakeRead",
				effect=iam.Effect.ALLOW,
				actions=[
					"cloudtrail:ListEventDataStores",
					"cloudtrail:StartQuery",
					"cloudtrail:GetQueryResults",
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
		
		cloudtrail_lake_read_role = iam.Role(
			self, 'cloudtrail-lake-read-role',
			role_name='cloudtrail-lake-read-role',
			description='CloudTrail Lake Read role to gather Run and gather query results for automation purposes',
			assumed_by=iam.CompositePrincipal(
				iam.ServicePrincipal('lambda.amazonaws.com'),
				iam.ServicePrincipal('ec2.amazonaws.com'),
				iam.ArnPrincipal(assume_arn_principal)
				),
			path='/security/'
		)

		cloudtrail_lake_read_role_policy.attach_to_role(cloudtrail_lake_read_role)