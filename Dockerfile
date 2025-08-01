# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including build tools for llama-cpp-python)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    cmake \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set compiler environment variables
ENV CC=gcc
ENV CXX=g++

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements and install all dependencies at once
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]