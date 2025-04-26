# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
COPY wait_for_db.py /app/wait_for_db.py
# Expose the port
EXPOSE 8000

# Run migrations, collect static, start server
CMD ["bash", "-c", "python wait_for_db.py && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 booking_system.wsgi:application"]