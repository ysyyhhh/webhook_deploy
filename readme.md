


```shell
docker build -t webhook_deploy .
docker run -d --name webhook_deploy --env-file .env -p 8078:8078 webhook_deploy
```