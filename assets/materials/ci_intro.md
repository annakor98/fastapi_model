# Введение в CI/CD

Добавить линтеры и тестирование для каждого push:

Создать ``.github/workflows/lint_and_test_on_push.yaml``

Указываем, что workflow запускается при push в репозиторий:

```yaml
on:
  push
```

Создаем окружение, в котором будет запускаться (Ubuntu, Python, poetry):

```yaml
jobs:
  run_lint_and_tests:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@master
    - name: Install Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        architecture: 'x64'
    - name: Install poetry
      uses: abatilo/actions-poetry@v2
```

Добавляем запуск линтеров и тестов с помощью ``Makefile``:

```yaml
  - name: Install the project dependencies
    run: poetry install
  - name: Run lint
    run: poetry run make lint
  - name: Run tests
    run: poetry run make test
```

<details>
<summary><b> Все вместе </b></summary>

```yaml
# .github/workflow/lint_and_test_on_push.yaml

on:
  push

jobs:
  run_lint_and_tests:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@master
    - name: Install Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        architecture: 'x64'
    - name: Install poetry
      uses: abatilo/actions-poetry@v2
    - name: Install the project dependencies
      run: poetry install
    - name: Run lint
      run: poetry run make lint
    - name: Run tests
      run: poetry run make test
```