FROM python:3.11 AS build

RUN pip install poetry
COPY poetry.lock pyproject.toml .
RUN poetry export --only main --no-cache -o requirements.txt
RUN pip install -r requirements.txt --target=packages --no-cache-dir

FROM python:3.11-slim

COPY --from=build packages /usr/lib/python3/site-packages
ENV PYTHONPATH=/usr/lib/python3/site-packages
WORKDIR /app
COPY src/ /app

CMD ["python", "-m", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]

