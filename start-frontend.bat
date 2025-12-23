@echo off
echo Opening Money Transfer System Frontend...
cd frontend
start http://localhost:8000
python -m http.server 8000
