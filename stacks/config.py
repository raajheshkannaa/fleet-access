'''
This could easily be a wildcard and no necessary to hardcode this. However for the sake of security :P we make sure only this account can assume the Org Read Only Role and the Spoke Role. The automation master account from where the automation is run from or where the hub role is present.
'''
HUB_ACCOUNT = '<SECURITY OR AUTOAMATION ACCOUNT ID>' 
ORG_ACCOUNT = '<BILLING ACCOUNT ID>'
