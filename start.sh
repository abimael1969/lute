#!/bin/bash
# Railway deployment startup script

echo "=== Lute Startup ==="
echo "PORT: ${PORT:-not set}"
echo "PWD: $(pwd)"
echo ""

# Create data directories FIRST (before any app initialization)
mkdir -p /app/data /app/data/backups

echo "=== Data directory ==="
df -h /app/data 2>/dev/null || echo "df failed"
ls -la /app/data/

echo ""
echo "=== Data directory disk usage ==="
du -sh /app/data/* 2>/dev/null || echo "du failed"

echo ""
echo "=== Language definitions ==="
if [ -d "/app/lute/db/language_defs" ]; then
    echo "Found language_defs:"
    ls /app/lute/db/language_defs/ | head -10
else
    echo "ERROR: language_defs not found!"
fi

echo ""
echo "=== Starting Lute on port ${PORT:-5001} ==="
exec python -m lute.main --port ${PORT:-5001}