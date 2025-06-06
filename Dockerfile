# Use Python 3.11 slim image as base
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install uv and dependencies in a single layer
RUN apt-get update && \
    apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy requirements, model files, and API server
COPY requirements.txt pyproject.toml metadata.json ./
COPY model/ ./model/
COPY serve_model.py .

# Install dependencies
RUN which uv && \
    uv pip install --system -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose API port
EXPOSE 8000

# Command to run the API server
CMD ["python", "serve_model.py"]
