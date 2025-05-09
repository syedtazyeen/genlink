#!/bin/bash
set -e

echo "📦 Building PROD stack..."
docker-compose -f docker-compose.prod.yml up --build
