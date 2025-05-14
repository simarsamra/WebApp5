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
    # libpq-dev is for PostgreSQL. Remove if only using SQLite.
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Copy entrypoint script and make it executable
# Place it in /app for simplicity
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static files at build time
# Your entrypoint.sh also runs collectstatic, which is fine.
# Ensure this runs from the correct context if manage.py is nested
RUN python battery_manager/manage.py collectstatic --noinput

# Change working directory to where manage.py is
WORKDIR /app/battery_manager

# Expose port
EXPOSE 8000

# Start server using entrypoint script now located at /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]