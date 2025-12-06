# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY docling_server.py .
COPY api_server.py .

# Create directories for input and output
RUN mkdir -p /app/input /app/output

# Expose port for API
EXPOSE 8000

# Default command (can be overridden)
CMD ["python", "api_server.py"]
