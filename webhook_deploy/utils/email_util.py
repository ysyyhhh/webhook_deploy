import smtplib
from email.mime.text import MIMEText
from email.header import Header
import subprocess
import datetime
from webhook_deploy.utils import log_util
import webhook_deploy.config as config
logger = log_util.logger
def send_email(receivers:list,content:str,subject:str):
    # 第三方 SMTP 服务
    mail_host=config.MAIL_HOST  #设置服务器
    mail_user=config.MAIL_USER    #用户名
    mail_pass=config.MAIL_PASS
    
    
    sender = 'ysyy_test@163.com'
    # receivers 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "git_mooctest <"+sender+">"
    message['To'] =  receivers[0]
    
    message['Subject'] = Header(subject, 'utf-8')

    logger.info(message)
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host,port=465,timeout=10) # SMTP, linux  SMTP_SSL  465
        res = smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger.info("邮件发送成功")
    except Exception as e:
        logger.info(e)
        logger.info("Error: 无法发送邮件")

if __name__ == '__main__':
    email = "757578166@qq.com"
    branch = "rongrunxiang/click_active_cal"
    username = "ysyy"
    update_time = "2023-07-11T14:43:22+08:00"
    # send_email(update_time,username,branch,email)
    receivers = ['757578166@qq.com']
    content = '''ysyyhhh，您刚刚在DigitalMap项目中提交的分支wds/webhook_test在2023-09-15T09:17:45+08:00测试成功，请提交pull request 并 通知相关人员进行代码review
详情见 https://git.mooctest.com/digital-navigation-map/DigitalMap/compare/2608c36ee44269f26f7eae0830113523162842ef...16d08c0e49175d390b5b39058eaf5ae668aa3df0'''
    subject = 'git提交后的邮件检查结果发送测试'
    send_email(receivers,content,subject)