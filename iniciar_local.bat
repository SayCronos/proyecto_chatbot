@echo off
echo.
echo 🖥️  INICIANDO SERVIDOR EN MODO LOCAL
echo =====================================
echo.
echo 📍 Solo accesible desde esta computadora
echo 🌐 URL: http://127.0.0.1:8000
echo 💻 Chat: http://127.0.0.1:8000/chat
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo.
echo ⚠️  Para detener el servidor: Ctrl+C
echo.

REM Configurar variables de entorno para modo local
set HOST=127.0.0.1
set PUERTO=8000
set DEBUG=true

REM Iniciar servidor
python main_refactorizado.py

pause
