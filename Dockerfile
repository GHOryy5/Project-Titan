# Base Image: Lightweight Python Linux (Alpine)
FROM python:3.11-slim-bookworm

# Metadata
LABEL maintainer="TITAN LABS"
LABEL description="Asymmetric Warfare C2 Framework"
LABEL version="17.0"

# Set Working Directory
WORKDIR /app

# Install System Dependencies (GCC for compiling C crypto libs)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Project Files
COPY requirements.txt .
COPY setup.py .
COPY README.md .
COPY titan_core ./titan_core

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .

# Create Volume for Database Persistence
VOLUME /app/data

# Security: Create non-root user
RUN useradd -m operator
USER operator

# Entry Point
ENTRYPOINT ["python", "titan_core/main.py"]
