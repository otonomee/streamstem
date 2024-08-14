# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository and submodules
RUN git clone https://github.com/your-username/your-repo.git . && \
    git submodule update --init --recursive

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y torch torchaudio && \
    pip install --no-cache-dir torch==2.1.0+cpu torchaudio==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Install Demucs
RUN cd demucs && pip install -e . && cd ..

# Copy the rest of the application code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Create a shell script to run the application
RUN echo '#!/bin/bash\n\
exec gunicorn application:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --keep-alive 5 --log-level info\n'\
> /app/start.sh && chmod +x /app/start.sh

# Define the command to run the application
CMD ["/app/start.sh"]