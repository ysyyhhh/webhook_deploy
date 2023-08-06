# poetry run python main.py
# FROM --platform=linux/amd64 ubuntu:latest 
# python:3.8.5-slim-buster

FROM --platform=linux/amd64 python:3.8.5-slim-buster

WORKDIR /webhook_deploy

COPY pyproject.toml poetry.lock /webhook_deploy/

RUN mkdir -p ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf

RUN pip install poetry
RUN poetry install

COPY . /webhook_deploy/

ENTRYPOINT [ "poetry", "run"]

CMD ["uvicorn", "webhook_deploy.main:app", "--host=0.0.0.0", "--port=8078"]