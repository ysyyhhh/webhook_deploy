## 安装poetry

```shell
poetry install

```

## 环境变量

| 环境变量  | 说明             | 示例          |
| --------- | ---------------- | ------------- |
| LOG_PATH  | 日志文件存放路径 | D:\logs       |
| MAIL_HOST | 邮件服务器地址   | smtp.163.com  |
| MAIL_USER | 邮件发送者       | <xxx@163.com> |
| MAIL_PASS | 邮件发送者密码   | password      |

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
- name: project1
  deploy_sh_path: /home/project1/deploy.sh
  test_sh_path: /home/project1/test.sh
- name: project2
  deploy_sh_path: /home/project2/deploy.sh
EOF

```

## 启动

```shell

# 前台启动
poetry run uvicorn webhook_deploy.main:app --host 0.0.0.0 --port 8078

# 后台启动
nohup poetry run uvicorn webhook_deploy.main:app --host 0.0.0.0 --port 8078 > /nohup.out 2>&1 &

# 然后在webhook中配置http://ip:8078//webhook/event

```

## 在git中配置webhook地址

## 管理后台启动

```shell

# 查看后台日志 在/nohup.out

# 查看进行中的后台任务
lsof -i :8078

# 停止
kill -9 pid

```
