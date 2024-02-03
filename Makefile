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

.PHONY: ruff_fix
ruff_fix:
	ruff --fix ${PROJ_PATH} ${TESTS_PATH} ${ALEMBIC_PATH}

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
	pytest --cov-report term-missing --cov=app --durations=3
	pytest --dead-fixtures


.PHONY: tests_performance
tests_performance:
	make up
	sleep 3
	locust --config tests/performance/locust.conf
	make down


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


.PHONY: up_db
up_db:
	${DC} up --build -d --remove-orphans postgres


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
