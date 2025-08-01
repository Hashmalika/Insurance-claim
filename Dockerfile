# Use an official Python runtime
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run the application
CMD ["python", "app/main.py"]
