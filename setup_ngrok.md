# 🚀 Guía Rápida: ngrok (Solución Rápida)

## Paso 1: Instalar ngrok en Windows

1. Ve a: https://ngrok.com/download
2. Descarga ngrok para Windows
3. Extrae el archivo `ngrok.exe`
4. Crea cuenta en https://dashboard.ngrok.com/get-started/your-authtoken

## Paso 2: Configurar ngrok

En PowerShell (en la carpeta donde está ngrok.exe):
```powershell
.\ngrok config add-authtoken TU_TOKEN_AQUI
```

## Paso 3: Iniciar túnel

```powershell
.\ngrok http 8000
```

Verás algo como:
```
Forwarding  https://abc123-def456.ngrok-free.app -> http://localhost:8000
```

## Paso 4: Configurar en Termux

```bash
# Usa la URL HTTPS que ngrok te dio
export CURSOR_SERVER_URL='https://abc123-def456.ngrok-free.app'
export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'

# Hacer permanente
echo "export CURSOR_SERVER_URL='https://abc123-def456.ngrok-free.app'" >> ~/.bashrc
echo "export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'" >> ~/.bashrc
source ~/.bashrc
```

## Paso 5: Verificar

```bash
curl $CURSOR_SERVER_URL/health
# Deberías ver: {"status":"ok"}
```

## Nota Importante

⚠️ La URL de ngrok cambia cada vez que reinicias (plan gratis).
Si quieres URL permanente, necesitas plan de pago o usar Tailscale.
