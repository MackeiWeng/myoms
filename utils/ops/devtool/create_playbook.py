#-*- coding:utf-8 -*-

import base64
import datetime
from config.setting import Config
import os
import  yaml

def fast_task_init(json_data):
    time_stuk = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    # name = json_data["name"]
    # user = json_data["user"]
    # ip_list = json_data["ip"]
    scriptcontent = json_data["scriptcontent"]
    scripttype = json_data["scripttype"]
    scriptcontent = base64.b64decode(scriptcontent.encode("utf-8"))

    if scripttype == "shell":
        script_file_path = os.path.join(Config.ANSIBLE_SCRIPTS_PATH,"{}.sh".format(time_stuk))
    if scripttype ==  "python":
        script_file_path = os.path.join(Config.ANSIBLE_SCRIPTS_PATH, "{}.py".format(time_stuk))
    with open(script_file_path,"wb") as f:
        f.write(scriptcontent)

    # ip_list = ",".join(ip_list)
    # palybook_data = [
    #     {
    #         "hosts":ip_list,
    #         "remote_user":user,
    #         "tasks":[
    #             {
    #                 "name":name,
    #                 "script":script_file_path
    #             }
    #         ]
    #     }
    # ]
    # palybook_path = os.path.join(Config.ANSIBLE_PLAYBOOK_PATH,"{}.yml".format(time_stuk))
    # with open(palybook_path, 'w') as f:
    #     yaml.dump(palybook_data, f, default_flow_style=False)
    return script_file_path