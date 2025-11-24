#!/bin/bash

echo "========================================"
echo "  SmartRent - Iniciando Servidor"
echo "========================================"
echo ""

# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor backend en background
echo "Iniciando servidor backend en http://127.0.0.1:8000"
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Esperar un poco antes de iniciar el frontend
sleep 3

# Iniciar servidor frontend en background
echo "Iniciando servidor frontend en http://localhost:5173"
cd front
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  Servidores iniciados!"
echo "  Backend:  http://127.0.0.1:8000"
echo "  Frontend: http://localhost:5173"
echo "========================================"
echo ""
echo "Presiona Ctrl+C para detener los servidores"

# Esperar a que se presione Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

