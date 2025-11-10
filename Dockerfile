# WiFi Security Education Dashboard - Dockerfile
# Multi-stage build for optimized image size

# Build stage
FROM python:3.10-slim AS builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements-v2.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements-v2.txt

# Runtime stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    wireless-tools \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 dashboard && \
    mkdir -p /app && \
    chown -R dashboard:dashboard /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/dashboard/.local

# Copy application code
COPY --chown=dashboard:dashboard . .

# Switch to non-root user
USER dashboard

# Add local Python packages to PATH
ENV PATH=/home/dashboard/.local/bin:$PATH

# Expose no ports (local CLI application)

# Health check (verify Python and dependencies)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import rich, psutil, yaml; print('OK')" || exit 1

# Default command: run in mock mode
CMD ["python3", "main_v2.py"]

# Labels
LABEL maintainer="WiFi Security Education Project"
LABEL version="2.0.0"
LABEL description="Educational dashboard for WiFi security monitoring"
LABEL org.opencontainers.image.source="https://github.com/[your-user]/wifi_security_education"
