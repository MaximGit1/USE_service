# USE API & Run tasks service
___
## Information

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit/main.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit/main)

Project on the fastapi framework.

## All components of the application
- This is a main service (backend)
- [Run Task Service (backend)](https://github.com/MaximGit1/USE_run_serive)
- [Frontend](https://github.com/MaximGit1/USE_front)


___

## How to run

### Cloning the Repository
```
git clone https://github.com/MaximGit1/USE_service
cd USE_service
```

### Create migrations

```
alembic -c conf/alembic.ini revision --autogenerate -m ""
```
```
alembic -c conf/alembic.ini upgrade head
```

### Manage JWT

```
openssl genrsa -out certs/jwt-private.pem 2048
```
```
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```


### Configure and run
```
cp .env.dist .env
docker-compose up
```

Start files:
- src/use/run_api.py
- src/use/run_broker.py
