from aws_cdk import (
	aws_iam as iam,
)

import aws_cdk as cdk
from constructs import Construct
from stacks.config import HUB_ACCOUNT

class SpokeRoleStack(cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		
		super().__init__(scope, construct_id, **kwargs)

		spoke_role_policy = iam.ManagedPolicy(self, 'spoke-001-policy',
			managed_policy_name='spoke-001-policy',
			description='Policy for IAM Role used for Automation',
			statements = [
				iam.PolicyStatement(
					sid="SpokePolicyStatementIAM",
					effect=iam.Effect.ALLOW,
					actions=["iam:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementCF",
					effect=iam.Effect.ALLOW,
					actions=["cloudformation:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementCT",
					effect=iam.Effect.ALLOW,
					actions=["cloudtrail:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementConfig",
					effect=iam.Effect.ALLOW,
					actions=["config:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementLambda",
					effect=iam.Effect.ALLOW,
					actions=["lambda:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementSupport",
					effect=iam.Effect.ALLOW,
					actions=["support:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementWaf",
					effect=iam.Effect.ALLOW,
					actions=["waf:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementWaf02",
					effect=iam.Effect.ALLOW,
					actions=["waf-regional:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementShield",
					effect=iam.Effect.ALLOW,
					actions=["shield:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementGuardDuty",
					effect=iam.Effect.ALLOW,
					actions=["guardduty:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementInspector",
					effect=iam.Effect.ALLOW,
					actions=["inspector:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementElasticLoadBalancing",
					effect=iam.Effect.ALLOW,
					actions=["elasticloadbalancing:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementAPIGateway",
					effect=iam.Effect.ALLOW,
					actions=["apigateway:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementCloudFront",
					effect=iam.Effect.ALLOW,
					actions=["cloudfront:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementSNS",
					effect=iam.Effect.ALLOW,
					actions=["sns:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementLogs",
					effect=iam.Effect.ALLOW,
					actions=["logs:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementFirehose",
					effect=iam.Effect.ALLOW,
					actions=["firehose:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementEvents",
					effect=iam.Effect.ALLOW,
					actions=["events:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementES",
					effect=iam.Effect.ALLOW,
					actions=["es:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementEC2",
					effect=iam.Effect.ALLOW,
					actions=["ec2:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementRedshift",
					effect=iam.Effect.ALLOW,
					actions=["redshift:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementRDS",
					effect=iam.Effect.ALLOW,
					actions=["rds:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementROUTE53",
					effect=iam.Effect.ALLOW,
					actions=["route53:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementROUTE53DOMAINS",
					effect=iam.Effect.ALLOW,
					actions=["route53domains:*"],
					resources=["*"],
					),
				iam.PolicyStatement(
					sid="SpokePolicyStatementS3",
					effect=iam.Effect.ALLOW,
					actions=[
						"s3:GetBucketLocation",
						"s3:GetBucketPolicy",
						"s3:GetBucketVersioning",
						"s3:GetEncryptionConfiguration",
						"s3:GetObject",
						"s3:GetObjectAcl",
						"s3:HeadBucket",
						"s3:ListAllMyBuckets",
						"s3:ListBucket",
						"s3:PutEncryptionConfiguration",
						"s3:PutBucketPolicy",
						"s3:PutBucketLogging",
						"s3:CreateBucket",
						"s3:DeleteBucketPolicy",
						"s3:PutLifecycleConfiguration",
						"s3:GetLifecycleConfiguration"								
					],
					resources=["*"],
					),												
			]		
		)
		assume_arn_principal = 'arn:aws:iam::' + HUB_ACCOUNT + ':role/security/hub-001' # This could easily be a wildcard and no necessary to hardcode this. However for the sake of security :P we make sure only this account can assume the Org Read Only Role

		spoke_role = iam.Role(
			self, 'spoke-001',
			role_name='spoke-001',
			assumed_by=iam.CompositePrincipal(
				iam.ServicePrincipal('lambda.amazonaws.com'),
				iam.ServicePrincipal('ec2.amazonaws.com'),
				iam.ArnPrincipal(assume_arn_principal)
			),
			path='/security/'
		)

		spoke_role_policy.attach_to_role(spoke_role)

		spoke_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('ReadOnlyAccess'))
		spoke_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AWSKeyManagementServicePowerUser'))
