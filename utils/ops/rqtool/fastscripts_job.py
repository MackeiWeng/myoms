# coding:utf-8
from rq import Queue
from redis import  Redis

# from utils.ops.devtool.ansible_tool import AnsibleTask
# from utils.ops.devtool.create_playbook import fast_task_init
# from config.setting import Config
from rq.decorators import job
from .fastscripts_worker import fastscripts_conn


@job('fastscripts', connection=fastscripts_conn)
def run_fastscripts_playbook(json_data):
    # hosts = ",".join(json_data["ip"])
    # user = json_data["user"]
    # script_file_path = fast_task_init(json_data)
    # extra_vars = {"hosts": hosts, "user": user, "script_path": script_file_path}
    # ansible_handle = AnsibleTask(json_data["ip"], extra_vars=extra_vars)
    # result = ansible_handle.exec_playbook(playbooks=[Config.ANSIBLE_FASTSCRIPT_PLAYBOOK_PATH])
    return json_data