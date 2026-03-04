#!/bin/bash

# ORGANISME SAAS OTONOM - Startup Script
echo "🧬 Initializing ORGANISME SAAS OTONOM (Gen-4)..."

# Kill existing processes on ports 8000 and 8080
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :8080) 2>/dev/null || true

# Start Backend
echo "🧠 Starting Backend (FastAPI) on port 8000..."
python3 -m backend.main > backend.log 2>&1 &

# Start Frontend
echo "👁️ Starting Frontend (Vite) on port 8080..."
npm run dev -- --host 127.0.0.1 --port 8080 > frontend.log 2>&1 &

echo "✅ Organism is now ALIVE."
echo "   Dashboard: http://127.0.0.1:8080"
echo "   API Docs:  http://127.0.0.1:8000/docs"
echo ""
echo "Monitor logs with: tail -f backend.log frontend.log"
