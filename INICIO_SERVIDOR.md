# 🚀 Cómo Iniciar el Servidor

## Método 1: Script Automático (Windows)

Simplemente ejecuta:
```bash
iniciar_servidor.bat
```

## Método 2: Manual (Windows PowerShell)

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Iniciar servidor
python start_server.py
```

## Método 3: Con uvicorn directamente

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar con uvicorn
uvicorn server.bridge_server:app --host 0.0.0.0 --port 8000
```

## Método 4: Linux/Mac

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor
python start_server.py
```

## Verificar que funciona

Una vez iniciado, deberías ver:
```
Iniciando servidor en http://0.0.0.0:8000
Presiona Ctrl+C para detener
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Abre en tu navegador: http://localhost:8000/health

Deberías ver: `{"status":"ok"}`

## Configuración

El servidor usa las siguientes configuraciones (en `.env`):

- `PORT=8000` - Puerto del servidor
- `CURSOR_WORKSPACE_PATH=.` - Ruta del workspace
- `API_TOKEN=change-me-in-production` - Token de autenticación

## Para acceso desde tu teléfono

1. **En la misma red local:**
   - Usa la IP de tu computadora: `http://192.168.1.X:8000`
   - Encuentra tu IP con: `ipconfig` (Windows) o `ifconfig` (Linux/Mac)

2. **Con ngrok (recomendado para pruebas):**
   ```bash
   ngrok http 8000
   # Usa la URL HTTPS que te da
   ```

3. **Con Tailscale (recomendado para producción):**
   ```bash
   tailscale up
   # Usa la IP de Tailscale
   ```

## Detener el servidor

Presiona `Ctrl+C` en la terminal donde está corriendo.
