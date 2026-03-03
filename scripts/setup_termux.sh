#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "== GPT-CodexBridge Termux setup =="

pkg update -y && pkg upgrade -y
pkg install -y python git curl nano ripgrep

python -m pip install --upgrade pip
python -m pip install "httpx>=0.28.0" "typer>=0.16.0" "rich>=14.0.0"

if [ ! -d "$HOME/GPT-CodexBridge" ]; then
  echo "Clona el repo en Termux (si aun no lo hiciste):"
  echo "  git clone https://github.com/TeoVMP/cursor-termux-bridge.git ~/GPT-CodexBridge"
fi

cat <<'EOF'
Variables recomendadas:
  export BRIDGE_SERVER_URL='http://IP_DE_TU_PC:8765'
  export BRIDGE_API_TOKEN='tu-token'

Para persistirlas:
  echo "export BRIDGE_SERVER_URL='http://IP_DE_TU_PC:8765'" >> ~/.bashrc
  echo "export BRIDGE_API_TOKEN='tu-token'" >> ~/.bashrc
  source ~/.bashrc
EOF

echo "== Setup completado =="
