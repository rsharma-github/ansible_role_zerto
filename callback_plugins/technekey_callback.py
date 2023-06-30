from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.plugins.callback import CallbackBase
from ansible import constants as C
from ansible.utils.color import colorize, hostcolor
from ansible.utils.display import Display

DOCUMENTATION = '''
    callback: verbose_retry
    type: stdout
    short_description: 
      1. Print the stdout and stderr during until/delay/retries
      2. Print the results during the loop for each item
    description:
      - During the retry of any task, by default the task stdout and stderr are hidden from the user on the terminal.
      - To make things more transparent, we are printing the stdout and stderr to the terminal. 
    requirements:
      - python subprocess,datetime,pprint
    '''



class CallbackModule(CallbackBase):

    '''
    Call all the runner functions here
    '''

    CALLBACK_VERSION = 2.0                          # you should use version 2.0 at the time of wrtiting this post
    CALLBACK_TYPE = 'notification'                  # you can only use 1 stdout plugin at a time, so used notification
    CALLBACK_NAME = 'loop_and_retry_verbose'        # name it anything, it probably does not matter.

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__()


    ##
    ## Start writing runner functions here as per the playbook 
    ## lifecycle

    def v2_playbook_on_start(self, playbook):
        self._display.display(playbook._name + " is started",color=C.COLOR_OK)    
        #self.playbook = playbook
        #print(playbook.__dict__)
    def v2_playbook_on_task_start(self, task, is_conditional):
        self._display.display(task._name + " is started",color=C.COLOR_OK)
        self.task = task
        print(task.__dict__)
