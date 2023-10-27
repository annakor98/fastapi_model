## Работа с Docker

Необходимые шаги:
1. Установить Docker Desktop
2. Залогиниться (через GitHub)
3. Убедиться, что Engine running

### Готовим Dockerfile

1. First stage (requirements-stage)
   1. Используем образ python
   2. Устанавливаем poetry
   3. Преобразуем требования из poetry в ``requirements.txt``
2. Second stage
   1. Устанавливаем ``requirements.txt``
   2. Копируем код
   3. Запускаем с помощью ``uvicorn``

```dockerfile
FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r /code/requirements.txt
COPY ./app /code/app
COPY ./.env /code/.env
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```
Далее готовим образ:

```commandline
docker build -t username/myimage .
```

И запускаем контейнер:

```commandline
docker run -d --name mycontainer -p 80:80 username/myimage
```

Проверяем результат на ``http://localhost:80/``

## Добавляем в GitHub Actions

1. Создать токен на DockerHub
2. Добавить токен в Secrets репозитория

```yaml
name: Deploy

on:
  push:
    branches:
    - '*'

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Login to Docker Hub
      run: echo ${{ secrets.DOCKER_PASS }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
    - name: build image
      run: docker build -t ${{ secrets.DOCKER_USERNAME }}/myimage .
    - name: push to Docker Hub
      run: docker push ${{ secrets.DOCKER_USERNAME }}/myimage:latest

```

Делаем так, чтобы workflow срабатывал после успешного выполнения ``ci.yaml`` (работает только в default branch)

В ``ci.yaml`` добавляем ``name``:
```yaml
name: Checks
```
Далее дорабатываем ``deploy.yaml``:

```yaml
name: Deploy

on:
  workflow_run:
    workflows: [Checks]
    types:
    - completed

  push:
    branches:
    - '*'

jobs:
  upload:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
    - uses: actions/checkout@master
    - name: Login to Docker Hub
      run: echo ${{ secrets.DOCKER_PASS }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
    - name: build image
      run: docker build -t ${{ secrets.DOCKER_USERNAME }}/myimage .
    - name: push to Docker Hub
      run: docker push ${{ secrets.DOCKER_USERNAME }}/myimage:latest

```
