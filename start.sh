#!/bin/bash
# Railway deployment startup script

echo "=== Lute Startup ==="
echo "PORT: ${PORT:-not set}"
echo "PWD: $(pwd)"
echo ""

echo "=== Config directory ==="
ls -la /app/lute/config/

echo ""
echo "=== Data directory ==="
mkdir -p /app/data /app/data/backups
ls -la /app/data

echo ""
echo "=== Starting Lute on port ${PORT:-5001} ==="
exec python -m lute.main --port ${PORT:-5001}