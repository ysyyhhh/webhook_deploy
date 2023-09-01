
## 环境变量
|环境变量|说明|示例|
|--|--|--|
|LOG_PATH|日志文件存放路径|D:\logs|
|DEPLOY_SH_PATH|部署脚本路径|D:\deploy.sh|
|TEST_SH_PATH|测试脚本路径|D:\test.sh|
|MAIL_HOST|邮件服务器地址|smtp.163.com|
|MAIL_USER|邮件发送者|xxx@163.com|
|MAIL_PASS|邮件发送者密码|password|



```shell
git clone https://github.com/ysyyhhh/webhook_deploy.git
cd webhook_deploy
// 创建并编辑.env文件
cat > .env << EOF
LOG_PATH=/root/logs
DEPLOY_SH_PATH=/root/deploy.sh
TEST_SH_PATH=/root/test.sh
MAIL_HOST=smtp.163.com

sh deploy.sh
```