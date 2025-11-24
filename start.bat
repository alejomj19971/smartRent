@echo off
echo ========================================
echo   SmartRent - Iniciando Servidor
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Iniciar servidor backend
echo Iniciando servidor backend en http://127.0.0.1:8000
start "SmartRent Backend" cmd /k "python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000"

REM Esperar un poco antes de iniciar el frontend
timeout /t 3 /nobreak >nul

REM Iniciar servidor frontend
echo Iniciando servidor frontend en http://localhost:5173
cd front
start "SmartRent Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo   Servidores iniciados!
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul

