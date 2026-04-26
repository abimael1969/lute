#!/bin/bash
# Railway deployment startup script

echo "=== Lute Startup ==="
echo "PORT: ${PORT:-not set}"
echo "PWD: $(pwd)"
echo ""

echo "=== App lute directory ==="
ls -la /app/lute/

echo ""
echo "=== Lute db directory ==="
ls -la /app/lute/db/

echo ""
echo "=== Language definitions ==="
if [ -d "/app/lute/db/language_defs" ]; then
    echo "Found language_defs directory:"
    ls /app/lute/db/language_defs/ | head -20
    echo ""
    echo "=== Arabic definition ==="
    cat /app/lute/db/language_defs/arabic/definition.yaml 2>/dev/null | head -5 || echo "NOT FOUND!"
else
    echo "ERROR: language_defs directory not found!"
fi

echo ""
echo "=== Data directory ==="
mkdir -p /app/data /app/data/backups
ls -la /app/data

echo ""
echo "=== Starting Lute on port ${PORT:-5001} ==="
exec python -m lute.main --port ${PORT:-5001}