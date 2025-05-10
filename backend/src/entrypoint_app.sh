#!/bin/sh

set -e

echo "Running migrations..."
alembic upgrade head
echo "Migrations complete"

echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2