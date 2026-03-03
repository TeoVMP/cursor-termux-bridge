Write-Host "== GPT-CodexBridge server setup =="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python no esta instalado en PATH"
}

python -m venv .venv
& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e .\agent-server

if (-not (Test-Path ".env")) {
  Copy-Item ".\config\env.example" ".env"
  Write-Host "Se creo .env desde config/env.example"
}

Write-Host "Siguientes pasos:"
Write-Host "  1) Edita .env (token, roots, modelo)"
Write-Host "  2) Ejecuta: bridge-server"
