# Lute Dockerfile for Railway deployment
# Optimized for Railway's container runtime

FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    FLIT_ROOT_INSTALL=1

# Set work directory
WORKDIR /app

# Install system dependencies for natto-py (MeCab) and curl (for downloading language_defs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    libmecab-dev \
    mecab \
    mecab-ipadic \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README_PyPi.md ./
COPY lute/ ./lute/

# Download and extract language definitions if not present
RUN if [ ! -f "lute/db/language_defs/arabic/definition.yaml" ]; then \
        rm -rf lute/db/language_defs && \
        curl -sL https://github.com/LuteOrg/lute-language-defs/archive/refs/heads/master.tar.gz | \
        tar -xz && \
        mv lute-language-defs-master lute/db/language_defs; \
    fi

# Create required directories for persistent storage
RUN mkdir -p /app/data /app/data/backups

# Copy production config as config.yml
COPY lute/config/config.yml.prod /app/lute/config/config.yml

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install flit && \
    flit install --only-deps --deps production

# Expose port
EXPOSE 5001

# Run the application via startup script
CMD ["/app/start.sh"]