@echo off
echo Iniciando servidor Cursor-Termux Bridge...
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Iniciar servidor
python start_server.py

pause
