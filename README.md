Zerto
=========

This role perform zerto FOTE, SO and SB operations for one or more VPGs.

Requirements
------------

Before using this role must have zerto accees (zerto IP, user and password).

Role Variables
--------------

zvm_ipaddress,zvm_vpg_name,zvm_username and zvm_password

Dependencies
------------

Zerto zvm should rechable from ansible.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

	- hosts: localhost
		gather_facts: true
		roles:
		- zerto
		
License
-------

BSD

Author Information
------------------
radhe.tyche@gmail.com

Input File - input.json
-----------------------
{
   "zerto":{
      "infra":{
         "zvm_ipaddress":"X.X.X.X",
         "zvm_port":3664,
         "zvm_vpg_name":[
            "SEVPG","TRVPG"
         ]
      },
      "user":{
         "zvm_username":"",
         "zvm_password":""
      },
      "resource":{
         "mem":{
            "size":126,
            "unit":"mb"
         },
         "cpu":{
            "cores":2,
            "cap":1
         }
      },
      "operations":{
         "wait_time":60,
         "retry":5,
         "initial_delay":30,
         "delay":60,
         "time_unit":"sec"
      }
   }
}


Steps to execute the role
-----------------------------
ansible-playbook zerto/zerto_role_playbook.yml -e '@input.json'

Steps to run the callback
-----------------------------
1: coupy the callback_plugins folder parallel to playbook (zerto_role_playbook.yml).
2: ansible-playbook zerto/zerto_role_playbook.yml -e '@input.json'