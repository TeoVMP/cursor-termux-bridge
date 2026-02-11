#!/data/data/com.termux/files/usr/bin/bash
# Script para corregir las variables de entorno en Termux

echo "=== Corrigiendo Variables de Entorno ==="
echo ""

# Verificar variables actuales
echo "Variables actuales:"
echo "  CURSOR_SERVER_URL='$CURSOR_SERVER_URL'"
echo "  API_TOKEN='$API_TOKEN'"
echo ""

# Limpiar variables (eliminar cualquier pipe o caracteres extra)
unset CURSOR_SERVER_URL
unset API_TOKEN

# Configurar correctamente (sin pipes ni caracteres extra)
export CURSOR_SERVER_URL='http://10.92.178.225:8000'
export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'

echo "Variables corregidas:"
echo "  CURSOR_SERVER_URL='$CURSOR_SERVER_URL'"
echo "  API_TOKEN='$API_TOKEN'"
echo ""

# Limpiar .bashrc de líneas incorrectas
echo "Limpiando ~/.bashrc..."
sed -i '/export CURSOR_SERVER_URL=/d' ~/.bashrc
sed -i '/export API_TOKEN=/d' ~/.bashrc

# Añadir líneas correctas
echo "export CURSOR_SERVER_URL='http://10.92.178.225:8000'" >> ~/.bashrc
echo "export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'" >> ~/.bashrc

echo "✓ Variables guardadas en ~/.bashrc"
echo ""

# Probar conexión
echo "Probando conexión..."
if curl -s "$CURSOR_SERVER_URL/health" > /dev/null; then
    echo "✓ Conexión exitosa!"
    curl "$CURSOR_SERVER_URL/health"
else
    echo "✗ No se pudo conectar"
    echo "  Verifica que el servidor esté corriendo"
fi

echo ""
echo "Para aplicar los cambios en esta sesión:"
echo "  source ~/.bashrc"
