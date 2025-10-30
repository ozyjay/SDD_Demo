#!/bin/bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf src/build 2>/dev/null || true

echo "📁 Creating build directory..."
mkdir -p src/build/web

echo "🔨 Building with pygbag..."
python -m pygbag --build src/main.py

echo "🌐 Starting server on port 3496..."
cd src/build/web
python -m http.server 3496