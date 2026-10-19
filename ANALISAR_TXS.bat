@echo off
chcp 65001 >nul
cls
echo ========================================
echo 🔍 ANÁLISE FORENSE DE TRANSAÇÕES
echo ========================================
echo.
echo Analisando 3 TXs do contrato:
echo 0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079
echo.
echo Isso vai mostrar:
echo   - Dados básicos de cada TX
echo   - Input data decodificado
echo   - Logs e eventos
echo   - Transfers de tokens
echo   - Transações internas
echo   - Conclusão do que aconteceu
echo.
echo ========================================
echo.

py analisar_transacoes.py

pause
