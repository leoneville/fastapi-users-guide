FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-root

EXPOSE 8000
CMD [ "gunicorn", "--bind=0.0.0.0:8000", "fastapi_users_guide.app:app", "-w", "4", "-k", "uvicorn_worker.UvicornWorker" ]