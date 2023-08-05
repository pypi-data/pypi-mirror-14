
# Import opinel
from opinel.utils import *


########################################
##### Helpers
########################################

#
# Connect to EC2 API
#
def connect_ec2(key_id, secret, session_token,  region_name):
    return connect_service('ec2', key_id, secret, session_token, region_name)

#
# Connect to ELB API
#
def connect_elb(key_id, secret, session_token, region_name):
    return connect_service('elb', key_id, secret, session_token, region_name)


########################################
##### Helpers
########################################

#
# Get name from tags
#
def get_name(local, remote, default_attribute):
    name_found = False
    if 'Tags' in remote:
        for tag in remote['Tags']:
            if tag['Key'] == 'Name':
                local['name'] = tag['Value']
                name_found = True
    if not name_found:
        local['name'] = remote[default_attribute]
