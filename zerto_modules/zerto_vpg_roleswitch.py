#!/usr/bin/python
#Module to do ZertoRoleSwitch by providing the vpg_vpgidentifier
#Author: Radheyshyam
#Input:zvm_ipaddress,session_key and vpg_vpgidentifier
#Output:task_id
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###Functions####
def main():
    module = AnsibleModule(
        argument_spec=dict(
            vpg_vpgidentifier = dict(type='str', required=True,),
            zvm_ipaddress = dict(type='str', required=True),
            session_key = dict(type= 'str', required=True),
            operation = dict(type= 'str', required=True)
        ),
       supports_check_mode = False
    )
    vpg_vpgidentifier = module.params['vpg_vpgidentifier']
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    operation = module.params['operation']
    base_url = f"https://{zvm_ip}:9669/v1"
    vpgs_url = f"{base_url}/vpgs"
    msg = "Successful VPG " + operation + " complete."

    def doZertoRoleSwitch():

        # Creating Header with x-zerto-session
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-zerto-session': api_key
        }
        
        #Create Body for RoleSwitch request
        body = {
           'CommitPolicy': '1',
           'ShutdownPolicy': '1',
           'TimeToWaitBeforeShutdownInSec': '0',
           'IsReverseProtection': 'true'
        }
        
        body = json.dumps(body)
    
        url = vpgs_url + '/' + vpg_vpgidentifier + '/Failover'
        print("RoleSwitch URL:: " + url)
        # Do roleswitch_response by providing the vpg_vpgidentifier
        roleswitch_response = requests.post(url, data=body, headers=headers, verify=False)
        return ""
        if roleswitch_response.ok:
            roleswitch_response = roleswitch_response.json()
            print("roleswitch_response:: " + roleswitch_response)
            return roleswitch_response

    result_task_id = doZertoRoleSwitch()
    module.exit_json(changed=True, task_id = msg)

from ansible.module_utils.basic import *
main()
