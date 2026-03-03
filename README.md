# GPT-CodexBridge

Bridge de IA para orquestar desarrollo desde Termux contra repos en PC, usando un modelo local servido por LM Studio.

## Objetivo

Este proyecto implementa una arquitectura cliente-servidor:

- `termux-client`: CLI para Android/Termux.
- `agent-server`: servidor local que expone herramientas seguras de archivos, busqueda y shell.
- Adapter LLM compatible con endpoint OpenAI de LM Studio.

## Estado

La primera version incluye:

- Loop basico de tool-calling.
- Herramientas: `read_file`, `write_file`, `apply_patch`, `glob`, `rg_search`, `run_shell`, `git_status`, `git_diff`.
- Politicas de seguridad por rutas y comandos.
- Auditoria en JSONL.
- Flujo de aprobacion y modo `plan-first`.

## Estructura

```text
agent-server/
  src/bridge_server/
termux-client/
  src/bridge_cli/
docs/
```

## Requisitos

- Python 3.11+
- `rg` (ripgrep) disponible en host servidor
- LM Studio corriendo API local compatible OpenAI (por defecto `http://127.0.0.1:1234/v1`)

## Quickstart

1. Setup del servidor (Windows PowerShell):
   - `powershell -ExecutionPolicy Bypass -File .\scripts\setup_server.ps1`
2. Editar `.env` con:
   - `BRIDGE_API_TOKEN`
   - `BRIDGE_ALLOWED_ROOTS`
   - `BRIDGE_MODEL_NAME` y URL de LM Studio
3. Levantar servidor:
   - `bridge-server`
4. Setup de Termux:
   - `bash scripts/setup_termux.sh`
   - `bash scripts/configure_termux.sh`
5. Probar desde cliente:
   - `bridge status`
   - `bridge chat --project /ruta/del/proyecto --message "lista archivos python"`

## Operacion remota

- ngrok: ver `docs/setup_ngrok.md`
- Tailscale: ver `docs/setup_tailscale.md`
- Publicacion GitHub: ver `docs/github_publish.md`

## Seguridad

- El servidor no ejecuta fuera de `allowed_roots`.
- El endpoint RPC exige `x-bridge-token` cuando `BRIDGE_API_TOKEN` esta configurado.
- `run_shell` requiere aprobacion para comandos peligrosos.
- Timeouts de shell y limites de salida habilitados por defecto.
- Todas las acciones quedan en `logs/audit.jsonl`.
