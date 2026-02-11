# 🚀 Guía Rápida: Tailscale

## Paso 1: Instalar en Windows (Computadora)

1. Ve a: https://tailscale.com/download/windows
2. Descarga e instala Tailscale
3. Abre Tailscale y crea cuenta/inicia sesión
4. Conecta

## Paso 2: Obtener IP de Tailscale

En PowerShell o CMD:
```powershell
tailscale ip
```

Te dará algo como: `100.64.123.45`

## Paso 3: Instalar en Android (Teléfono)

1. Instala Tailscale desde Google Play Store
2. Inicia sesión con la misma cuenta
3. Conecta

## Paso 4: Configurar en Termux

```bash
# Obtén la IP de tu computadora (ejecuta tailscale ip en Windows)
# Luego en Termux:
export CURSOR_SERVER_URL='http://100.64.123.45:8000'
export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'

# Hacer permanente
echo "export CURSOR_SERVER_URL='http://100.64.123.45:8000'" >> ~/.bashrc
echo "export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'" >> ~/.bashrc
source ~/.bashrc
```

## Paso 5: Verificar

```bash
curl $CURSOR_SERVER_URL/health
# Deberías ver: {"status":"ok"}
```

¡Listo! Ahora puedes conectarte desde cualquier lugar.
