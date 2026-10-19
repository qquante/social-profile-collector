@echo off
chcp 65001 >nul
cls
echo ========================================
echo MoltX Sniper - Teste Rápido
echo ========================================
echo.

echo [1/3] Removendo venv quebrado...
if exist "venv" (
    rmdir /s /q venv
    echo     ✓ Venv removido!
)

echo.
echo [2/3] Criando novo venv...
py -m venv venv
if errorlevel 1 (
    echo ERRO ao criar venv! Tentando com python...
    python -m venv venv
)
echo     ✓ Venv criado!

echo.
echo [3/3] Instalando requests...
venv\Scripts\pip.exe install requests
echo     ✓ Requests instalado!

echo.
echo ========================================
echo Executando teste...
echo ========================================
echo.

venv\Scripts\python.exe quick_test.py

echo.
echo ========================================
echo Pronto! Verifique os arquivos gerados.
echo ========================================
pause
