#!/data/data/com.termux/files/usr/bin/bash
# Script de configuración rápida para Termux

echo "=== Configuración de Cursor-Termux Bridge ==="
echo ""

# Verificar si ya está configurado
if [ -n "$CURSOR_SERVER_URL" ] && [ -n "$API_TOKEN" ]; then
    echo "Ya tienes configuración existente:"
    echo "  CURSOR_SERVER_URL=$CURSOR_SERVER_URL"
    echo "  API_TOKEN=$API_TOKEN"
    echo ""
    read -p "¿Quieres reconfigurar? (s/n): " reconfigure
    if [ "$reconfigure" != "s" ] && [ "$reconfigure" != "S" ]; then
        echo "Configuración cancelada."
        exit 0
    fi
fi

echo "Paso 1: URL del servidor"
echo "Ejemplos:"
echo "  - Red local: http://192.168.1.100:8000"
echo "  - ngrok: https://abc123.ngrok.io"
echo ""
read -p "Ingresa CURSOR_SERVER_URL: " server_url

echo ""
echo "Paso 2: Token de autenticación"
echo "Este token debe ser el mismo que está en el archivo .env del servidor"
echo ""
read -p "Ingresa API_TOKEN: " api_token

# Validar que no estén vacíos
if [ -z "$server_url" ] || [ -z "$api_token" ]; then
    echo "Error: URL y Token son requeridos"
    exit 1
fi

# Configurar para esta sesión
export CURSOR_SERVER_URL="$server_url"
export API_TOKEN="$api_token"

# Añadir a .bashrc
echo ""
read -p "¿Hacer permanente (añadir a ~/.bashrc)? (s/n): " make_permanent

if [ "$make_permanent" = "s" ] || [ "$make_permanent" = "S" ]; then
    # Eliminar líneas anteriores si existen
    sed -i '/export CURSOR_SERVER_URL=/d' ~/.bashrc
    sed -i '/export API_TOKEN=/d' ~/.bashrc
    
    # Añadir nuevas líneas
    echo "export CURSOR_SERVER_URL='$server_url'" >> ~/.bashrc
    echo "export API_TOKEN='$api_token'" >> ~/.bashrc
    
    echo ""
    echo "✓ Configuración guardada en ~/.bashrc"
fi

echo ""
echo "=== Configuración completada ==="
echo ""
echo "Variables configuradas:"
echo "  CURSOR_SERVER_URL=$CURSOR_SERVER_URL"
echo "  API_TOKEN=$api_token"
echo ""

# Probar conexión
echo "Probando conexión con el servidor..."
if curl -s -f "$server_url/health" > /dev/null; then
    echo "✓ Conexión exitosa!"
else
    echo "⚠ No se pudo conectar al servidor"
    echo "  Verifica que el servidor esté corriendo"
    echo "  Verifica que la URL sea correcta"
fi

echo ""
echo "Para usar el cliente:"
echo "  cursor query 'tu pregunta'"
