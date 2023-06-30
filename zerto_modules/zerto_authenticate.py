#!/usr/bin/python
#Module to generate the x-zerto-session
#Author: Radheyshyam
#Input:zvm_ipaddress,zvm_username and zvm_password
#Output:zerto_apikey
import requests 
import json 
from requests.auth import HTTPBasicAuth 


DOCUMENTATION = r'''
---
module: zerto_authenticate
short_description: Provide the zerto x-session
description:
  - Interacts with the zero ZVM using the zerto REST API and provide the x-session.
  - This modile need zerto_authentication before generating the zerto z-session.
version_added: "1.1"
author: radhe.tyche@gmail.com
options:
    zvm_ipaddress:
        description: Valid ZVM IP which is required for login the ZERTO and get the x-session.
        required: true
        type: str
    zvm_username:
        description:
            - Valid ZVM user-name which is required for login the ZERTO and get the x-session.
        required: true
        type: str
    zvm_password:
        description:
            - Valid ZVM password which is required for login the ZERTO and get the x-session.
        required: true
        type: str
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  zerto_authenticate_output.zerto_apikey:
    name: x-session
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The zvm_ip, zvm_user and zvm_password  param that was passed in.
    type: str
    returned: always
    sample: 'zvm_ip=x.x.x.x, zvm_user=user-name and zvm_password=******'
message:
    description: The output message that the zerto_authenticate  module generates.
    type: str
    returned: always
    sample: 'x-session: 29ea4a08b4af82b1110419be610d4f0d32eccb61'
'''


def main(): 
    print("Getting start ZVM API token...")
    module = AnsibleModule(
        argument_spec=dict(
            zvm_password = dict(type='str', required=True, no_log=True),
            zvm_ipaddress = dict(type='str', required=True), 
            zvm_username = dict(type= 'str', required=True)
        ), 
       supports_check_mode = False 
    )
    zvm_ip = module.params['zvm_ipaddress']
    zvm_u = module.params['zvm_username']
    zvm_p = module.params['zvm_password']
    base_url = "https://"+zvm_ip+":9669/v1"
    session = base_url+"/session/add"
    print("session url:: " + session)

    def login(session_url, zvm_user, zvm_password, module):
        print("Getting ZVM API token for login...")
        auth_info = "{\r\n\t\"AuthenticationMethod\":1\r\n}"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(session_url, headers=headers, data=auth_info, verify=False, auth=HTTPBasicAuth(zvm_user, zvm_password))
        if response.ok: 
            auth_token = response.headers['x-zerto-session']
            print("Api Token: " + auth_token)
            return auth_token
        else: 
            module.fail_json(msg=("HTTP %i - %s, Message %s" % (response.status_code, response.reason, response.text)))   

    returned_token = login(session, zvm_u, zvm_p, module)
    module.exit_json(changed=True, zerto_apikey=returned_token)

from ansible.module_utils.basic import *
main()
