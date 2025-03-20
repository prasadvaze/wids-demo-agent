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
    POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
WORKDIR /app

FROM base AS bulder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc pipx

ENV PATH="/root/.local/bin:${PATH}"

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade "pip==24.0" && \
    pip install pipx && \
    pipx install "poetry==$POETRY_VERSION" && \
    pipx inject poetry poetry-plugin-bundle

COPY pyproject.toml poetry.lock ./

RUN touch README.md && poetry bundle venv --python=/usr/bin/python3 --only=main /venv

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1


