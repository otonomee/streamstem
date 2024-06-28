FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD gunicorn application:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT