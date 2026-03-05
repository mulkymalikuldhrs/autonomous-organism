#!/bin/bash

# Bunuh proses yang sudah ada di port 8000 dan 8080
echo "Cleaning up ports..."
kill $(lsof -t -i :8000) 2>/dev/null || true
kill $(lsof -t -i :8080) 2>/dev/null || true

# Jalankan backend
echo "Starting backend..."
uvicorn backend.main:app --host 127.0.0.1 --port 8000 > backend.log 2>&1 &

# Tunggu backend siap
sleep 5

# Jalankan frontend
echo "Starting frontend..."
npm run dev > frontend.log 2>&1 &

echo "Organisme SaaS Otonom is running!"
echo "Dashboard: http://localhost:8080"
echo "API: http://localhost:8000"
echo "Logs: backend.log, frontend.log"
