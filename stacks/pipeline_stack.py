from aws_cdk import (
	aws_codecommit as codecommit,
	pipelines as pipelines,
	aws_iam as iam,
)

import aws_cdk as cdk
from constructs import Construct
from .hub_org_deploy import HubandOrgRolePipelineStage
from .spoke_deploy import SpokeRolePipelineStage

class FleetAccessPipelineStack(cdk.Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		# Create a codecommit repository called 'FleetAccess'
		repo = codecommit.Repository(
			self, 'FleetAccess',
			repository_name='FleetAccess'
		)

		pipeline = pipelines.CodePipeline(
			self, 'Pipeline',
			pipeline_name='FleetAccess-Pipeline',
			cross_account_keys=True,
			synth=pipelines.ShellStep("Synth",
				input=pipelines.CodePipelineSource.code_commit(repo, 'master'),
				commands=[
					"npm install -g aws-cdk",
					"pip install -r requirements.txt",
					"npx cdk synth"
					],
				),
			code_build_defaults=pipelines.CodeBuildOptions(
				role_policy=[iam.PolicyStatement(
					actions=['organizations:ListAccounts'],
					sid='AllowListAccounts',
					effect=iam.Effect.ALLOW,
					resources=['*'],
				)],				
			)
		)
	

		deploy_stage1 = pipeline.add_stage(HubandOrgRolePipelineStage(
			self, 'HubandOrgRoleDeployment'
			))
		
		deploy_stage2 = pipeline.add_stage(SpokeRolePipelineStage(
		self, 'SpokeRoleDeployment'
		))
