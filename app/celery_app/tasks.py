# -*- coding: utf-8 -*-

from utils.ops.celerytool.main import celery_app
from utils.ops.devtool.create_playbook import fast_task_init
# from utils.ops.devtool.ansible_tool import AnsibleTask
from config.setting import Config
from celery.utils.log import  get_task_logger

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
from utils.ops.devtool.callback import AdHocResultCallback
import ansible.constants as C
'''
在我们第一次执行远程操作时, 会有一个交互, 要求填写一个yes/no, 确认是将连接的host 写入 known_hosts
那我们如何取消这个交互呢'''
C.HOST_KEY_CHECKING = False

from celery.utils.log import  get_task_logger

logger = get_task_logger(__name__)



class PlaybookResultCallBack(CallbackBase):
    """
    Custom callback model for handlering the output data of
    execute playbook file,
    Base on the build-in callback plugins of ansible which named `json`.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'Dict'

    def __init__(self, display=None):
        super(PlaybookResultCallBack, self).__init__(display)
        self.results = []
        self.output = ""
        self.item_results = {}  # {"host": []}

    def _new_play(self, play):
        return {
            'play': {
                'hosts': play.name,
                'id': str(play._uuid)
            },
            'tasks': []
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.get_name(),
            },
            'hosts': {}
        }

    def v2_playbook_on_no_hosts_matched(self):
        self.output = "skipping: No match hosts."

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        '''
        :param task: 名字不能为Gathering Facts
        :param is_conditional:
        :return:
        '''
        if task.get_name() != "Gathering Facts":
            self.results[-1]['tasks'].append(self._new_task(task))

    def v2_playbook_on_play_start(self, play):
        self.results.append(self._new_play(play))
        logger.info("run v2_playbook_on_play_start")
        logger.info(self.results)

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        if self.output:
            pass
        else:
            self.output = {
                'plays': self.results,
                'stats': summary
            }

    def gather_result(self, res):
        if not res._result.get("ansible_facts"):
            tmp_result = {
                "stdout": [],
                "stderr": [],
                "rc": 0,
                "start": "",
                "end": ""
            }
            if res._result.get('stderr_lines', None):
                tmp_result["stderr"].extend(res._result['stderr_lines'])
            if res._result.get("stdout_lines", None):
                tmp_result["stdout"].extend(res._result["stdout_lines"])
            if res._result.get("rc", None):
                tmp_result["rc"] = res._result["rc"]
            if res._result.get("start", None):
                tmp_result["start"] = res._result["start"]
            if res._result.get("end", None):
                tmp_result["end"] = res._result["end"]

            self.results[-1]['tasks'][-1]['hosts'][res._host.name] = tmp_result
            logger.info(111111111)
            logger.info(self.results)

    def v2_runner_on_ok(self, res, **kwargs):
        self.gather_result(res)
        logger.info(111111111)
        logger.info(self.results)

    def v2_runner_on_failed(self, res, **kwargs):
        self.gather_result(res)

    def v2_runner_on_unreachable(self, res, **kwargs):
        self.gather_result(res)

    def v2_runner_on_skipped(self, res, **kwargs):
        self.gather_result(res)

    def gather_item_result(self, res):
        self.item_results.setdefault(res._host.name, []).append(res._result)

    def v2_runner_item_on_ok(self, res):
        self.gather_item_result(res)

    def v2_runner_item_on_failed(self, res):
        self.gather_item_result(res)

    def v2_runner_item_on_skipped(self, res):
        self.gather_item_result(res)


class AnsibleTask:
    def __init__(self, hosts, extra_vars=None,timeout=None):
        Options = namedtuple('Options', [
            'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
            'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
            'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
            'scp_extra_args', 'become', 'become_method', 'become_user',
            'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
            'diff', 'gathering', 'remote_tmp',
        ])
        self.hosts = hosts
        self._validate()
        self.hosts_file = None
        self.timeout = 100 if not timeout else timeout
        self.options = Options(
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            timeout=self.timeout,
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
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=[','.join(self.hosts)+','])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if extra_vars:
            self.variable_manager.extra_vars = extra_vars

        logger.info(self.options)

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

        logger.info(getattr(getattr(playbook, '_tqm'),"_stdout_callback"))

        playbook.run()

        return results_callback

    def __del__(self):
        if self.hosts_file:
            os.remove(self.hosts_file)



@celery_app.task
def run_fastscripts(json_data):

    hosts = ",".join(json_data["ip"])
    user = json_data["user"]
    script_file_path = fast_task_init(json_data)
    extra_vars = {"hosts": hosts, "user": user, "script_path": script_file_path}
    ansible_handle = AnsibleTask(json_data["ip"], extra_vars=extra_vars)
    results_callback = ansible_handle.exec_playbook(playbooks=[Config.ANSIBLE_FASTSCRIPT_PLAYBOOK_PATH])
    result = results_callback.results
    return  result