@echo off
echo.
echo 📱 INICIANDO SERVIDOR EN MODO RED LOCAL
echo ========================================
echo.

REM Obtener IP local
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do (
    for /f "tokens=1" %%j in ("%%i") do (
        set LOCAL_IP=%%j
        goto :found
    )
)
:found

echo 🌐 Accesible desde otros dispositivos en la red
echo 📍 IP Local: %LOCAL_IP%
echo 🖥️  URL Local: http://127.0.0.1:8000
echo 📱 URL Red: http://%LOCAL_IP%:8000
echo 💬 Chat: http://%LOCAL_IP%:8000/chat
echo 📚 API Docs: http://%LOCAL_IP%:8000/docs
echo.
echo ⚠️  IMPORTANTE: Asegúrate de que el firewall permita el puerto 8000
echo 🔥 Comando firewall: New-NetFirewallRule -DisplayName "FastAPI Port 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
echo.
echo ⚠️  Para detener el servidor: Ctrl+C
echo.

REM Configurar variables de entorno para modo red
set HOST=0.0.0.0
set PUERTO=8000
set DEBUG=false

REM Iniciar servidor
python main_refactorizado.py

pause
