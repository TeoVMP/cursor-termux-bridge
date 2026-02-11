#!/usr/bin/env bash
# Script de instalación para el servidor (computadora)
# Ejecuta: bash setup_server.sh

set -e

echo "=== Configuración del Servidor Bridge ==="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    exit 1
fi

echo "1. Verificando Python..."
python3 --version

# Crear entorno virtual (opcional pero recomendado)
if [ ! -d "venv" ]; then
    echo ""
    echo "2. Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
if [ -d "venv" ]; then
    echo ""
    echo "3. Activando entorno virtual..."
    source venv/bin/activate || source venv/Scripts/activate
fi

# Instalar dependencias
echo ""
echo "4. Instalando dependencias Python..."
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv requests

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo ""
    echo "5. Creando archivo .env..."
    cp config/env.example .env
    echo "✓ Archivo .env creado. Por favor, edítalo con tus configuraciones."
fi

# Crear directorio para base de datos de sesiones
mkdir -p data

echo ""
echo "=== Instalación completada ==="
echo ""
echo "Para iniciar el servidor:"
echo "  source venv/bin/activate  # o venv/Scripts/activate en Windows"
echo "  python server/bridge_server.py"
echo ""
echo "O con uvicorn directamente:"
echo "  uvicorn server.bridge_server:app --host 0.0.0.0 --port 8000"
echo ""
echo "Para acceso remoto seguro, considera usar:"
echo "  - ngrok: ngrok http 8000"
echo "  - tailscale: tailscale up"
echo "  - SSH tunnel: ssh -R 8000:localhost:8000 usuario@servidor"
echo ""
