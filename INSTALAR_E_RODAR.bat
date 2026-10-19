@echo off
chcp 65001 >nul
cls
echo ========================================
echo MoltX Sniper - Setup Completo
echo ========================================
echo.

echo [1/4] Baixando get-pip.py...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 2>nul
if errorlevel 1 (
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
)
echo     ✓ Arquivo baixado!

echo.
echo [2/4] Instalando pip...
py get-pip.py --quiet
echo     ✓ PIP instalado!

echo.
echo [3/4] Instalando requests...
py -m pip install requests --quiet
echo     ✓ Requests instalado!

echo.
echo [4/4] Executando teste...
echo ========================================
echo.

py quick_test.py

echo.
echo.
echo ========================================
echo Limpando arquivos temporários...
del get-pip.py 2>nul

echo.
echo ========================================
echo Pronto! Verifique:
echo   - lauki_page_test.html
echo ========================================
pause
