![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Sanchoyzer/starlab)
![GitHub last commit](https://img.shields.io/github/last-commit/Sanchoyzer/starlab)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?logo=githubactions&logoColor=white)](https://github.com/Sanchoyzer/starlab/actions)
[![Sentry](https://img.shields.io/static/v1?message=Sentry&color=362D59&logo=Sentry&logoColor=FFFFFF&label=)](https://sentry.io)

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

## Starlab ##

Web service with REST API for creating and managing books

Technologies and libraries: python, aiohttp, alembic, postgres, sqlalchemy, gunicorn, sentry, docker, pytest, linters

CI: [GitHub Actions](https://github.com/Sanchoyzer/starlab/actions)

[Docker Hub](https://hub.docker.com/repository/docker/sanchoyzer/starlab)


### Technologies ###

- [python](https://www.python.org/)
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [poetry](https://python-poetry.org/docs/)
- [make](https://www.gnu.org/software/make/)


### How to ... ###

#### ... run application ####
`make up`

#### ... stop application ####
`make down`

#### ... check logs ####
`make logs`

#### ... run tests ####
`make tests`

#### ... run linters (locally) ####
`make check`

#### ... find Swagger UI ####
[Swagger UI](http://0.0.0.0:8081/docs)

#### ... find OpenAPI schema ####
[OpenAPI schema](http://0.0.0.0:8081/docs/spec)
