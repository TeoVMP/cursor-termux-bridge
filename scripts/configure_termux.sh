#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "== Configuracion interactiva Termux =="

read -p "BRIDGE_SERVER_URL (ej: http://192.168.1.10:8765): " server_url
read -p "BRIDGE_API_TOKEN: " api_token

if [ -z "$server_url" ] || [ -z "$api_token" ]; then
  echo "Error: ambos valores son obligatorios"
  exit 1
fi

export BRIDGE_SERVER_URL="$server_url"
export BRIDGE_API_TOKEN="$api_token"

sed -i '/export BRIDGE_SERVER_URL=/d' ~/.bashrc
sed -i '/export BRIDGE_API_TOKEN=/d' ~/.bashrc
echo "export BRIDGE_SERVER_URL='$server_url'" >> ~/.bashrc
echo "export BRIDGE_API_TOKEN='$api_token'" >> ~/.bashrc

echo "Variables guardadas en ~/.bashrc"
echo "Prueba rapida:"
echo "  bridge status"
