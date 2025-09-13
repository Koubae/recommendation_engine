FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates tar xz-utils \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh -s \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

FROM base AS builder

WORKDIR /app
COPY . ./
RUN uv sync --frozen --no-cache

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"

FROM builder AS development

WORKDIR /app
RUN uv sync --frozen --no-cache --all-groups

CMD ["bash"]


FROM builder AS production

WORKDIR /app
COPY recommendation_engine ./recommendation_engine
