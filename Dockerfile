FROM python:3.13.0-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev

RUN --mount=type=cache,target=/roo/.cache/uv \
  uv sync --frozen --no-dev

FROM python:3.13.0-slim-bookworm

RUN groupadd -g 1000 app && \
  useradd -u 1000 -g app -m app

WORKDIR /app

ENV PORT=8000
EXPOSE $PORT

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
  build-essential \
  libpq-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

RUN chmod +x ./entrypoint.sh

USER app

CMD ["./entrypoint.sh"]
