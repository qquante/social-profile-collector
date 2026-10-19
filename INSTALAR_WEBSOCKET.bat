@echo off
chcp 65001 >nul
cls
echo ========================================
echo Instalando WebSocket Client
echo ========================================
echo.

py -m pip install websocket-client

echo.
echo ========================================
echo Instalação concluída!
echo ========================================
pause
