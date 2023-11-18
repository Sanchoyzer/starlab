PROJ_PATH      ?= app
TESTS_PATH     ?= tests
ALEMBIC_PATH   ?= alembic

CONTAINER_APP  ?= app

DC             ?= docker compose
ALEMBIC        ?= alembic


### linters ###

.PHONY: black
black:
	black ${PROJ_PATH} ${TESTS_PATH} ${ALEMBIC_PATH}

.PHONY: ruff
ruff:
	ruff ${PROJ_PATH} ${TESTS_PATH} ${ALEMBIC_PATH}

.PHONY: mypy
mypy:
	mypy ${PROJ_PATH} ${TESTS_PATH} ${ALEMBIC_PATH}

.PHONY: bandit
bandit:
	bandit -c pyproject.toml --silent -r ${PROJ_PATH}

.PHONY: check
check: black ruff mypy bandit


### tests ###

.PHONY: tests
tests:
	TARGET=test ${DC} up --build --remove-orphans --exit-code-from app


### poerty wrappers ###

.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update

.PHONY: export_all
export_all:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with=test,dev


### local dev ###

.PHONY: up
up:
	${DC} up --build -d --remove-orphans


.PHONY: up_live
up_live:
	${DC} up --build --remove-orphans


.PHONY: down
down:
	${DC} down


.PHONY: restart
restart:
	${DC} down
	${DC} up --build -d --remove-orphans


.PHONY: logs
logs:
	${DC} logs -f -n 200


.PHONY: shell
shell:
	${DC} exec app bash


.PHONY: migration_create
migration_create:
	${ALEMBIC} revision --autogenerate -m "new"


.PHONY: migration_upgrade
migration_upgrade:
	${ALEMBIC} upgrade head
