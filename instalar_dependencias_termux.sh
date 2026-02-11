#!/data/data/com.termux/files/usr/bin/bash
# Script para instalar dependencias en Termux

echo "=== Instalando dependencias para Cursor-Termux Bridge ==="
echo ""

# Verificar que pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Instalando pip..."
    pkg install -y python-pip
fi

# Actualizar pip
echo "Actualizando pip..."
pip3 install --upgrade pip

# Instalar dependencias del cliente (solo las necesarias para Termux)
echo ""
echo "Instalando dependencias Python..."
pip3 install requests click python-dotenv

echo ""
echo "=== Verificando instalación ==="
python3 -c "import requests; import click; import dotenv; print('✓ Todas las dependencias instaladas correctamente')"

echo ""
echo "=== Instalación completada ==="
echo ""
echo "Ahora puedes usar:"
echo "  cursor query 'tu pregunta'"
