FROM python:3.12.9-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]