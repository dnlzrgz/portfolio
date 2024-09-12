FROM python:3.12.6-slim-bookworm

RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
  build-essential \
  libpq-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.dev.txt /
RUN pip install --no-cache-dir -r /requirements.dev.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail . .

USER wagtail

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
