# pull official base image
FROM python:3.12.9-slim-bookworm AS base
# set environment variables

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \ 
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_VERSION=25.0.1 \
    PIPX_VERSION=1.7.1 \
    POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get -y install netcat-traditional gcc postgresql \
  && apt-get clean

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade "pip==$PIP_VERSION" && \
    python3 -m pip install --user "pipx==$PIPX_VERSION" && \
    python3 -m pipx install "poetry==$POETRY_VERSION" && \
    python3 -m pipx inject poetry poetry-plugin-bundle && \ 
    touch README.md && \
    poetry bundle venv --with test /venv

COPY ./app /usr/src/app

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

USER app

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

