#!/bin/bash

# 🧬 ORGANISME SAAS OTONOM - START SCRIPT
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     🧬 ORGANISME SAAS OTONOM - STARTING...             ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Kill existing processes on ports 8000 and 8080
echo "🧹 Cleaning up ports..."
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :8080) 2>/dev/null || true

# Check for backend requirements
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: backend/requirements.txt not found."
    exit 1
fi

# Ensure output directories exist
mkdir -p products
mkdir -p growth_outbox

# Start Backend
echo "🚀 Starting Backend (FastAPI) on port 8000..."
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
until curl -s http://127.0.0.1:8000/api/metrics > /dev/null; do
  sleep 2
done
echo "✅ Backend is ready."

# Start Frontend
echo "🎨 Starting Frontend (Vite) on port 8080..."
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "-------------------------------------------------------------"
echo "🧬 ORGANISME IS ALIVE!"
echo "📡 Backend: http://127.0.0.1:8000"
echo "🌐 Frontend: http://127.0.0.1:8080"
echo "📜 Logs: backend.log, frontend.log"
echo "-------------------------------------------------------------"
echo "Press Ctrl+C to stop the organism."

# Handle exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
