@echo off
chcp 65001 >nul
cls
echo ========================================
echo 🔗 MONITOR ON-CHAIN - BASE NETWORK
echo ========================================
echo.
echo Monitorando compras de tokens do contrato:
echo 0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079
echo.
echo Quando comprar token novo:
echo   🔊 Apita 8x com 888 Hz por 888 ms cada
echo   📊 Mostra detalhes do token
echo   💾 Salva no histórico
echo.
echo ========================================
echo.

py monitor_onchain.py

pause
