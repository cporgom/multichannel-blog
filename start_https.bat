@echo off
TITLE MultiChannel Blog
CLS

:: 1. venv
CD /D "%~dp0"

:: 2. Activamos el entorno virtual
IF EXIST "venv\Scripts\activate.bat" (
    CALL venv\Scripts\activate.bat
) ELSE (
    ECHO [ERROR] No se encuentra la carpeta 'venv'.
    ECHO Por favor, asegúrate de haber creado el entorno virtual.
    PAUSE
    EXIT
)

:: 3. AUTO-REPARACIÓN
ECHO.
ECHO [INFO] Verificando e instalando librerias faltantes...
pip install -r requirements.txt

:: 4. Auto open
ECHO.
ECHO [INFO] Abriendo navegador...
START "" "https://127.0.0.1:5000"

:: 5. Start
ECHO.
ECHO [INFO] Iniciando servidor en el puerto 5000...
ECHO [INFO] Pulsa CTRL + C para detenerlo.
ECHO.
python app.py

:: 6. Pausa por si hay errores
El servidor se ha detenido.
PAUSE