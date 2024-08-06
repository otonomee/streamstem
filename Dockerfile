FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Set the default port to 8000 if not provided
ENV PORT 8000

# Command to run the application
CMD ["gunicorn", "application:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:$PORT"]