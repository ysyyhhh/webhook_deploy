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
    except smtplib.SMTPException:
        logger.info("Error: 无法发送邮件")

def send_test_result_email(update_time:str,username:str,branch:str, email:str,result):
    if result == 1:
        subject = "测试失败！" + username + "，您刚刚提交的分支{}测试失败，请检查并修复后再提交".format(branch)
        content = username + "，您刚刚提交的分支{}在{}测试失败，请检查并修复后再提交".format(branch,update_time)
    else:
        subject = "测试通过！" + username + "，您刚刚提交的分支{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(branch)
        content = username + "，您刚刚提交的分支{}在{}测试成功，请提交pull request 并 通知相关人员进行代码review".format(branch,update_time)
    logger.info(email)
    logger.info(subject)
    logger.info(content)
    send_email([email],content,subject)
    return result

if __name__ == '__main__':
    email = "757578166@qq.com"
    branch = "rongrunxiang/click_active_cal"
    username = "ysyy"
    update_time = "2023-07-11T14:43:22+08:00"
    test_and_send_email(update_time,username,branch,email)
    # receivers = ['757578166@qq.com']
    # content = '自动化邮件发送测试...'
    # subject = 'git提交后的邮件检查结果发送测试'
    # send_email(receivers,content,subject)