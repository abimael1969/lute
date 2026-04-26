# Lute Dockerfile for Railway deployment
# Optimized for Railway's container runtime

FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    FLIT_ROOT_INSTALL=1 \
    PORT=5001

# Set work directory
WORKDIR /app

# Install system dependencies for natto-py (MeCab)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    libmecab-dev \
    mecab \
    mecab-ipadic \
    && rm -rf /var/lib/apt/lists/*

# Copy project files first (needed for flit install)
COPY pyproject.toml README_PyPi.md ./
COPY lute/ ./lute/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install flit && \
    flit install --only-deps --deps production

# Create required directories for Railway persistent storage
RUN mkdir -p /app/data /app/backups

# Expose port (Railway uses PORT env var)
EXPOSE ${PORT:-5001}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-5001}/')" || exit 1

# Run the application
CMD ["python", "-m", "lute.main"]