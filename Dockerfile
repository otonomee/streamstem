# Base Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Python deps (app + demucs + torch CPU)
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r requirements.txt && \
    python -m pip install torch==2.1.2 torchaudio==2.1.2 -f https://download.pytorch.org/whl/torch_stable.html && \
    python -m pip install demucs

# App code
COPY . .

# Expose for web mode; CLI scripts can override the CMD
EXPOSE 8000

# Default: run the web app; for CLI use: docker run --rm -it streamstem bash straightBash.sh
CMD ["gunicorn", "application:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "120", "--keep-alive", "5", "--log-level", "info"]