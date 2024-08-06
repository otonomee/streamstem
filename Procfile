release: python setup.py
web: gunicorn application:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT