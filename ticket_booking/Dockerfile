# Use a slim Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && apt-get clean

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt  .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files (after dependencies are installed to cache layers)
COPY . .  

# Expose port 8000
EXPOSE 8000

# Default command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
