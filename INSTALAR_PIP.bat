@echo off
chcp 65001 >nul
cls
echo ========================================
echo Instalando PIP no Python
echo ========================================
echo.

echo [1/3] Baixando get-pip.py...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
if errorlevel 1 (
    echo ERRO ao baixar! Tentando com PowerShell...
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
)
echo     ✓ Arquivo baixado!

echo.
echo [2/3] Instalando pip...
py get-pip.py
if errorlevel 1 (
    python get-pip.py
)
echo     ✓ PIP instalado!

echo.
echo [3/3] Instalando requests...
py -m pip install requests
echo     ✓ Requests instalado!

echo.
echo Limpando arquivos temporários...
del get-pip.py

echo.
echo ========================================
echo PIP instalado com sucesso!
echo Agora pode rodar: py quick_test.py
echo ========================================
pause
