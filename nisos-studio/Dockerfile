FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from context (repository root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire nisos-studio folder into the container
COPY nisos-studio/ .

# Expose the port Starlette runs on
EXPOSE 8000

# Set Python path to ensure 'src' is importable
ENV PYTHONPATH=/app

# Command to run the application
CMD ["python", "src/agent/app.py"]
