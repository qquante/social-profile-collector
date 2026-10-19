@echo off
chcp 65001 >nul
cls
echo ========================================
echo 🔗 MONITOR ON-CHAIN TEMPO REAL
echo ========================================
echo.
echo WebSocket - Base Network
echo Contrato: 0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079
echo.
echo Detecta compras em TEMPO REAL:
echo   - Quando enviar USDC
echo   - Quando receber token novo
echo   - Alerta instantâneo!
echo.
echo ========================================
echo.

py monitor_onchain_wss.py

pause
