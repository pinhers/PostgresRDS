# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and templates
COPY app.py .
COPY templates/ ./templates/

# Expose Flask port
EXPOSE 5000

# Run Flask
CMD ["python", "app.py"]

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
