#!/usr/bin/python
#Module to check the VpgIdentifier exist or not
#Author: Radheyshyam
#Input:zvm_ipaddress,session_key and vpg_name
#Output:isVpgExist
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###Functions####
def main():
    module = AnsibleModule(
        argument_spec=dict(
            vpg_name = dict(type='str', required=True,),
            zvm_ipaddress = dict(type='str', required=True),
            session_key = dict(type= 'str', required=True)
        ),
       supports_check_mode = False
    )
    vpg = module.params['vpg_name']
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    base_url = f"https://{zvm_ip}:9669/v1"
    vpgs_url = f"{base_url}/vpgs"

    def isVpgExist():

        # Creating Header with x-zerto-session
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-zerto-session': api_key
        }

        # Gather VPG IDs from ZVM API
        vpg_response = requests.get(vpgs_url, headers=headers, verify=False)
        if vpg_response.ok:
            vpg_list = vpg_response.json()

        else:
            module.fail_json(msg=("HTTP %i - %s, Message %s" % (vpg_response.status_code, vpg_response.reason, vpg_response.text)))

        vpg_length = len(vpg_list)

        x=0
        isFound = False
        while True:
            try:
                for i in range(vpg_length):

                    for key, value in vpg_list[x].items():
                        if key == 'VpgName':
                            if value == vpg:  # Once VpgName and VpgIdentifier match, print the VPG name and ID
                                vpg_id = str(vpg_list[x]['VpgIdentifier'])
                                print('VPG found - VPG :: ' + value + ', VPG ID :: ' + vpg_id)
                                isFound = True

                    x = x + 1
            except IndexError:  # Break after x exceeds index length of vpg_list
                break
        return isFound
    return_isFound = isVpgExist()
    module.exit_json(changed=True, isVpgExist=return_isFound )

from ansible.module_utils.basic import *
main()
