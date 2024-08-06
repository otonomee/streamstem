# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt, 
# then uninstall torch and torchaudio, and reinstall CPU-only versions
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y torch torchaudio && \
    pip install --no-cache-dir torch==2.1.0+cpu torchaudio==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variable
ENV PORT 8000

# Create a shell script to run the application
RUN echo '#!/bin/bash\n\
exec gunicorn application:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT\n'\
> /app/start.sh && chmod +x /app/start.sh

# Define the command to run the application
CMD ["/app/start.sh"]