#!/usr/bin/python
#Module to do FailoverTest clean-up by providing the vpg_vpgidentifier
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
            session_key = dict(type= 'str', required=True)
        ),
       supports_check_mode = False
    )
    vpg_vpgidentifier = module.params['vpg_vpgidentifier']
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    base_url = f"https://{zvm_ip}:9669/v1"
    vpgs_url = f"{base_url}/vpgs"

    def doZertoFailoverTestStop():

        # Creating Header with x-zerto-session
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-zerto-session': api_key
        }
        url = vpgs_url + '/' + vpg_vpgidentifier + '/FailoverTestStop'
        print("FOTE URL:: " + url)
        # Do FailoverTest clean-up by providing the vpg_vpgidentifier
        fote_response = requests.post(url, headers=headers, verify=False)
        if fote_response.ok:
            fote_response_data = fote_response.json()
            print("fote_response_data:: " + fote_response_data)
            return fote_response_data

    result_task_id= doZertoFailoverTestStop()
    module.exit_json(changed=True, task_id="Successful VPG Failover Test stop")

from ansible.module_utils.basic import *
main()
