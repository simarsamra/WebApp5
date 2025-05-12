# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files and run migrations at build time
RUN python battery_manager/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start server using uvicorn (ASGI)
CMD python battery_manager/manage.py migrate && python -m uvicorn battery_manager.asgi:application --host 0.0.0.0 --port 8000