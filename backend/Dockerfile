FROM python:3.12.10-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip poetry setuptools wheel

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --without dev,test

COPY src .

RUN chmod +x entrypoint_app.sh

CMD ["./entrypoint_app.sh"]
