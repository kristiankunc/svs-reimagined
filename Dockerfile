FROM python:3-slim-bookworm

ARG DOCKER_BUILDING=true

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    pip install --no-cache-dir -r requirements.txt && \
    python manage.py tailwind install && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


ENV PORT=8096
EXPOSE ${PORT}

RUN python manage.py tailwind install --no-package-lock --no-input && \
    python manage.py tailwind build --no-input && \
    python manage.py collectstatic --no-input;

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 svs.wsgi:application