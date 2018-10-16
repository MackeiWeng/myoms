#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.plugins.callback.json import  CallbackModule
from callback import PlaybookResultCallBack,AdHocResultCallback,CommandResultCallback
import ansible.constants as C
'''
在我们第一次执行远程操作时, 会有一个交互, 要求填写一个yes/no, 确认是将连接的host 写入 known_hosts
那我们如何取消这个交互呢'''
C.HOST_KEY_CHECKING = False

Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user',
    'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
    'diff', 'gathering', 'remote_tmp',
])


def get_default_options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=10,
        remote_user='root',
        private_key_file='/root/.ssh/id_rsa',
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options


class AnsibleTask:
    def __init__(self, hosts, extra_vars=None):
        self.hosts = hosts
        self._validate()
        self.hosts_file = None
        self.options = get_default_options()
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=[','.join(self.hosts)+','])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if extra_vars:
            self.variable_manager.extra_vars = extra_vars

    def _validate(self):
        if not self.hosts:
            raise Exception('hosts不能为空')
        if not isinstance(self.hosts, list):
            raise Exception('hosts只能为list<AnsibleHost>数组')


    def exec_shell(self, command):
        source = {'hosts': 'all', 'gather_facts': 'no', 'tasks': [
            {'action': {'module': 'shell', 'args': command}, 'register': 'shell_out'}]}
        play = Play().load(source, variable_manager=self.variable_manager, loader=self.loader)
        results_callback = AdHocResultCallback()
        # results_callback = CallbackModule()
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords={},
                stdout_callback=results_callback
            )
            tqm.run(play)
            # return results_callback.results
            return results_callback.results_raw
        except:
            raise
        finally:
            if tqm is not None:
                tqm.cleanup()

    def exec_playbook(self, playbooks):
        results_callback = PlaybookResultCallBack()
        playbook = PlaybookExecutor(playbooks=playbooks, inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.options, passwords={})
        setattr(getattr(playbook, '_tqm'), '_stdout_callback', results_callback)
        playbook.run()
        return results_callback.results


    def __del__(self):
        if self.hosts_file:
            os.remove(self.hosts_file)

# if __name__ == "__main__":
#     host_list =  ['192.168.132.137',"192.168.132.140"]
#     ansible_handle = AnsibleTask(host_list)
#     print(ansible_handle.exec_shell(command="ls /opt"))
#     # print(ansible_handle.exec_playbook(playbooks=['/opt/mycode/script.yml']))