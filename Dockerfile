FROM python:3.11-slim

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]