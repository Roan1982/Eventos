# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install pipenv/poetry if you use them — here we'll use requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (uncomment if you use staticfiles and have settings configured)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Default command: run Gunicorn as WSGI server
# Ensure gunicorn is in your requirements.txt
CMD ["gunicorn", "event_platform.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
