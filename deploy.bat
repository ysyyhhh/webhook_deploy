docker stop webhook_deploy
docker rm webhook_deploy
docker build -t webhook_deploy .
docker run --network host -d --name webhook_deploy --env-file .env -p 8078:8078 webhook_deploy
