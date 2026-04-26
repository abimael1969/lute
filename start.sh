#!/bin/bash
# Railway deployment startup script

echo "=== Lute Startup ==="
echo "PORT: ${PORT:-not set}"
echo "PWD: $(pwd)"
echo ""

echo "=== App directory ==="
ls -la /app/

echo ""
echo "=== Lute module ==="
ls -la /app/lute/

echo ""
echo "=== Language definitions ==="
ls -la /app/lute/db/language_defs/ | head -20

echo ""
echo "=== Arabic definition ==="
cat /app/lute/db/language_defs/arabic/definition.yaml 2>/dev/null || echo "Arabic definition not found!"

echo ""
echo "=== Data directory ==="
mkdir -p /app/data /app/data/backups
ls -la /app/data

echo ""
echo "=== Starting Lute on port ${PORT:-5001} ==="
exec python -m lute.main --port ${PORT:-5001}