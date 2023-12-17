FROM python:3.11.7-slim as base
RUN python -m pip install --upgrade --no-cache-dir pip wheel setuptools \
    && python -m pip install poetry \
    && poetry config virtualenvs.create false \
    && mkdir -p /srv/src \
    && rm -rf /root/.cache

ENV PYTHONPATH=/srv/src
WORKDIR /srv/src

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --without=dev,test  \
    && rm -rf /root/.cache

COPY app ./app


FROM base as development
CMD gunicorn app.main:init_app --timeout 30 --workers 1 --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:8080 --log-file -


FROM base as test
RUN poetry install --only=test
COPY tests ./tests
CMD python -m pytest --cov-report term-missing --cov=app --durations=3 .


FROM base as production
CMD gunicorn app.main:init_app --timeout 120 --workers $(nproc) --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --log-file -


FROM base as migration
COPY alembic.ini ./
COPY alembic ./alembic
CMD alembic upgrade head && sleep 600
