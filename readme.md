
## 环境变量

|环境变量|说明|示例|
|--|--|--|
|LOG_PATH|日志文件存放路径|D:\logs|
|MAIL_HOST|邮件服务器地址|smtp.163.com|
|MAIL_USER|邮件发送者|<xxx@163.com>|
|MAIL_PASS|邮件发送者密码|password|

```shell
rm -rf webhook_deploy
git clone https://github.com/ysyyhhh/webhook_deploy.git
cd webhook_deploy
// 创建并编辑.env文件
cat > .env << EOF
LOG_PATH=/root/logs
MAIL_HOST=smtp.163.com
MAIL_USER=<xxx@163.com>
MAIL_PASS=password
EOF

// 创建projects.yaml
// test_sh_path是可选的，如果没有则不会执行测试脚本。
cat > projects.yaml << EOF
- name: DigitalMap
  deploy_sh_path: /home/centos/DigitalMap
  test_sh_path: /home/centos/DigitalMap/test.sh
- name: DigitalMapAdmin
  deploy_sh_path: /home/centos/DigitalMapAdmin
EOF



poetry run uvicorn webhook_deploy.main:app --host 0.0.0.0 --port 8078
```
