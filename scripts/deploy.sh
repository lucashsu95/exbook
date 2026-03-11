#!/bin/bash
set -euo pipefail

# ── 設定 ────────────────────────────────────────────────────────
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE="docker compose -f $APP_DIR/docker-compose.yml"

echo "========================================"
echo "  Exbook Deploy — $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# ── 建置 & 啟動 ────────────────────────────────────────────────
echo ""
echo "[1/3] Building images..."
$COMPOSE build --no-cache web

echo ""
echo "[2/3] Starting services..."
$COMPOSE up -d

echo ""
echo "[3/3] Checking health..."
sleep 5

# 確認所有容器都在跑
RUNNING=$($COMPOSE ps --status running --format json | python3 -c "
import sys, json
lines = sys.stdin.read().strip().split('\n')
count = sum(1 for l in lines if l.strip())
print(count)
")

EXPECTED=3
if [ "$RUNNING" -eq "$EXPECTED" ]; then
    echo "✓ All $EXPECTED services running."
else
    echo "✗ Expected $EXPECTED services, got $RUNNING."
    $COMPOSE ps
    exit 1
fi

echo ""
echo "Deploy complete."
