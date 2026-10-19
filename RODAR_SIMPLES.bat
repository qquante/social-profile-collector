@echo off
chcp 65001 >nul
cls
echo ========================================
echo MoltX Sniper - Teste SIMPLES (sem venv)
echo ========================================
echo.

echo Instalando requests no Python do sistema...
py -m pip install requests --quiet
if errorlevel 1 (
    python -m pip install requests --quiet
)

echo.
echo ========================================
echo Executando teste...
echo ========================================
echo.

py quick_test.py

echo.
echo ========================================
echo Pronto! Verifique o arquivo:
echo   lauki_page_test.html
echo ========================================
pause
