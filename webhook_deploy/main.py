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

def exec_command():
    
    command = "sh " + config.DEPLOY_SH_PATH
    logger.info("exec " + command + " ...")
    resp = os.system(command)
    logger.info(resp)

def exec_test_command(test_branch:str):
    if config.TEST_SH_PATH == None:
        # 没有测试脚本，直接返回通过
        return 0
    result = subprocess.run(["sh",config.TEST_SH_PATH,test_branch], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
    return result


def test_and_send_email(update_time:str,username:str,branch:str, email:str):
    # test
    result = exec_test_command(branch)
    
    if result == 1:
        subject = "测试失败！" + username + "，您刚刚提交的分支{}测试失败，请检查并修复后再提交".format(branch)
        content = username + "，您刚刚提交的分支{}在{}测试失败，请检查并修复后再提交".format(branch,update_time)
    else:
        subject = "测试通过！" + username + "，您刚刚提交的分支{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(branch)
        content = username + "，您刚刚提交的分支{}在{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(branch,update_time)
    logger.info(email)
    logger.info(subject)
    logger.info(content)
    
    # send email
    email_util.send_email([email],content,subject)
    return result


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/webhook/event")
async def receive_event(request: dict):
    logger.info(f"receive_event: {request}")
    if "ref" in request:
        logger.info("enter ref")
        update_time = request["repository"]["updated_at"]
        if "refs/heads/master" == request["ref"]:
            logger.info("send to merger")
            username = request["commits"][0]["author"]["username"]
            email = request["commits"][0]["author"]["email"]
        else:
            username = request["pusher"]["username"]
            email = request["pusher"]["email"]
        
        branch = request["ref"].replace("refs/heads/","")
        
        logger.info("update_time:{},username:{},email:{},branch:{}".format(update_time,username,email,branch))
        
        result = test_and_send_email(update_time,username,branch,email)

        logger.info("result:{}".format(result))
        if result == 0 and "refs/heads/master" == request["ref"]:
            exec_command()

    return {"status": "ok"}



# uvicorn.run(app, host="localhost", port=8077,access_log=True)
# nohup sudo uvicorn fastapi_deploy:app --host '0.0.0.0' --port 8077 &