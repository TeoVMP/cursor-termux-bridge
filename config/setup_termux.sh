#!/data/data/com.termux/files/usr/bin/bash
# Script de instalación para Termux
# Ejecuta: bash setup_termux.sh

set -e

echo "=== Configuración de Cursor-Termux Bridge en Termux ==="
echo ""

# Actualizar paquetes
echo "1. Actualizando paquetes..."
pkg update -y && pkg upgrade -y

# Instalar dependencias básicas
echo ""
echo "2. Instalando dependencias básicas..."
pkg install -y python git nano

# Verificar que nano está instalado
if ! command -v nano &> /dev/null; then
    echo "Error: nano no se pudo instalar"
    exit 1
fi
echo "✓ nano instalado"

# Instalar pip si no está disponible
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Instalando pip..."
    pkg install -y python-pip
fi

# Instalar librerías Python
echo ""
echo "3. Instalando librerías Python..."
pip install --upgrade pip
pip install requests click python-dotenv

# Crear directorio de configuración
echo ""
echo "4. Creando directorio de configuración..."
mkdir -p ~/.cursor_termux
mkdir -p ~/.cursor_termux/local_files
mkdir -p ~/.cursor_termux/.backup

# Verificar instalación
echo ""
echo "5. Verificando instalación..."
python3 --version
nano --version
git --version

echo ""
echo "=== Instalación completada ==="
echo ""
echo "Próximos pasos:"
echo "1. Copia el cliente a Termux:"
echo "   scp -r termux/ usuario@tu-ip:/data/data/com.termux/files/home/"
echo ""
echo "2. Configura las variables de entorno:"
echo "   export CURSOR_SERVER_URL='http://tu-servidor:8000'"
echo "   export API_TOKEN='tu-token'"
echo ""
echo "3. Haz el cliente ejecutable:"
echo "   chmod +x termux/cursor_client.py"
echo ""
echo "4. Crea un alias en ~/.bashrc:"
echo "   alias cursor='python3 ~/termux/cursor_client.py'"
echo ""
