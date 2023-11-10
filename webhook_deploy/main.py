'''
使用fastapi部署webhook，当gitlab上的master分支有更新时，自动执行command脚本
'''
from fastapi import FastAPI


import subprocess
from webhook_deploy.utils import email_util,log_util

import webhook_deploy.config as config

logger = log_util.logger

import os
app = FastAPI()
class Project:
    name: str
    deploy_sh_path: str
    test_sh_path: str
    
    
    def __init__(self,name,deploy_sh_path,test_sh_path):
        self.name = name
        self.deploy_sh_path = deploy_sh_path
        self.test_sh_path = test_sh_path

###
# 测试 是否能运行
##
def exec_run_test_command():
    if config.RUN_TEST_SH_PATH == None:
        # 没有测试脚本，直接返回通过
        logger.info("no run test sh")
        return 0
    command = "sh " + config.RUN_TEST_SH_PATH
    logger.info("exec " + command + " ...")
    resp = os.system(command)
    logger.info(resp)

exec_run_test_command()


def exec_command(project:Project):
    # command = "sh " + config.DEPLOY_SH_PATH
    command = "sh " + project.deploy_sh_path
    logger.info("exec " + command + " ...")
    resp = os.system(command)
    logger.info(resp)
    return resp

def exec_test_command(project:Project,test_branch:str):
    
    test_sh = project.test_sh_path
    if test_sh == None:
        # 没有测试脚本，直接返回通过
        return 0
    result = subprocess.run(["sh",test_sh,test_branch], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
    return result

def deploy_and_send_email(project:Project,update_time:str,username:str,branch:str, email:str,compare_url:str):
    # deploy
    result = exec_command(project)
    if result == 0:
        subject = "{} 部署成功！".format(project.name) + username + "，您刚刚在{}项目中提交的分支{}部署成功".format(project.name,branch)
        content = username + "，您刚刚在{}项目中提交的分支{}在{}部署成功".format(project.name,branch,update_time)
    else:
        subject = "{} 部署失败！".format(project.name) + username + "，您刚刚在{}项目中提交的分支{}部署失败，请检查并修复后再提交".format(project.name,branch)
        content = username + "，您刚刚在{}项目中提交的分支{}在{}部署失败，请检查并修复后再提交".format(project.name,branch,update_time)
    
    content += "\n详情见 {}".format(compare_url)
    
    # send email
    logger.info(result)
    logger.info(email)
    logger.info(subject)
    logger.info(content)
    email_util.send_email([email],content,subject)
    return result

def test_and_send_email(project:Project,update_time:str,username:str,branch:str, email:str,compare_url:str):
    # test
    result = exec_test_command(project,branch)
    
    if result == 1:
        subject = "测试失败！" + username + "，您刚刚在{}项目中提交的分支{}测试失败，请检查并修复后再提交".format(project.name,branch)
        content = username + "，您刚刚在{}项目中提交的分支{}在{}测试失败，请检查并修复后再提交".format(project.name,branch,update_time)
    else:
        subject = "测试通过！" + username + "，您刚刚在{}项目中提交的分支{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(project.name,branch)
        content = username + "，您刚刚在{}项目中提交的分支{}在{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(project.name,branch,update_time)
    
    content += "\n详情见 {}".format(compare_url)
    logger.info(email)
    logger.info(subject)
    logger.info(content)
    
    # send email
    email_util.send_email([email],content,subject)
    return result

projects = []


def get_project(name:str):
    for p in projects:
        if p.name == name:
            return p
    return None

@app.on_event("startup")
def load_project():
    # 从projects.yaml中加载项目信息
    global projects
    projects = []
    import yaml
    with open("projects.yaml") as f:
        tmp = yaml.load(f,Loader=yaml.FullLoader)
        print(tmp)
        for project in tmp:
            p = Project(project["name"],project["deploy_sh_path"],project.get("test_sh_path"))
            projects.append(p)
    for p in projects:
        logger.info(" ------------ ")
        logger.info(p.name)
        logger.info(p.deploy_sh_path)
        logger.info(p.test_sh_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/webhook/event")
async def receive_event(request: dict):
    logger.info(f"receive_event: {request}")
    
    project = get_project(request["repository"]["name"])
    
    if "ref" in request:
        logger.info("enter ref")
        update_time = request["repository"]["updated_at"]
        
        compare_url = request["compare_url"]
        
        is_master = False
        if "refs/heads/master" == request["ref"] or "refs/heads/main" == request["ref"]:
            logger.info("is main or master branch, send to merger")
            is_master = True
            username = request["commits"][0]["author"]["username"]
            email = request["commits"][0]["author"]["email"]
        else:
            logger.info("is not main or master branch, send to merger")
            username = request["pusher"]["username"]
            email = request["pusher"]["email"]
        
        branch = request["ref"].replace("refs/heads/","")
        
        logger.info("update_time:{},username:{},email:{},branch:{}".format(update_time,username,email,branch))
        
        result = test_and_send_email(project,update_time,username,branch,email,compare_url)

        logger.info("result:{}".format(result))
        if result == 0 and is_master:
            deploy_and_send_email(project,update_time,username,branch,email,compare_url)

    return {"status": "ok"}



# uvicorn.run(app, host="localhost", port=8077,access_log=True)
# nohup sudo uvicorn webhook_deploy:app --host '0.0.0.0' --port 8077 &

# poetry run uvicorn webhook_deploy.main:app --host '0.0.0.0' --port 8077