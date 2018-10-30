# -*- coding: utf-8 -*-

from utils.ops.celerytool.main import celery_app
from utils.ops.devtool.create_playbook import fast_task_init
from utils.ops.devtool.ansible_tool import AnsibleTask
from config.setting import Config


@celery_app.task
def run_fastscripts(json_data):
    hosts = ",".join(json_data["ip"])
    user = json_data["user"]
    script_file_path = fast_task_init(json_data)
    extra_vars = {"hosts": hosts, "user": user, "script_path": script_file_path}
    ansible_handle = AnsibleTask(json_data["ip"], timeout=json_data["timeout"], extra_vars=extra_vars)
    result = ansible_handle.exec_playbook(playbooks=[Config.ANSIBLE_FASTSCRIPT_PLAYBOOK_PATH])
    return  result