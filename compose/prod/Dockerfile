FROM debian:stable-20240926-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON=3.12.6
ENV PORT=8000

EXPOSE $PORT

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
  build-essential \
  libpq-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN uv sync --frozen --no-dev --no-install-project

RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]

