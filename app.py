#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.hub_role_stack import HubRoleStack
from stacks.spoke_role_stack import SpokeRoleStack
from stacks.org_read_only_role_stack import OrgReadOnlyRoleStack
from stacks.pipeline_stack import FleetAccessPipelineStack

from stacks.config import HUB_ACCOUNT, ORG_ACCOUNT

#hub_account_env = {	'account': HUB_ACCOUNT, 'region': 'us-east-1'}
org_account_env = {	'account': ORG_ACCOUNT, 'region': 'us-east-1'}
#cd_account_env = { 'account': CD_ACCOUNT, 'region': 'us-east-1'}

app = cdk.App()

FleetAccessPipelineStack(app, 'FleetAccessPipeline-Stack', env=org_account_env)

app.synth()
