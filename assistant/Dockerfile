FROM python:3.12-slim-bullseye

WORKDIR /opt/app
RUN adduser -D app_user
USER app_user

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE 0
ENV POETRY_NO_INTERACTION 1


RUN  pip install --upgrade pip && pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

CMD ["gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]