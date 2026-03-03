# Setup remoto con ngrok

## En PC

1. Instala ngrok y autenticalo.
2. Inicia el bridge server en `8765`.
3. Ejecuta:

```powershell
ngrok http 8765
```

4. Copia la URL `https://...ngrok...`.

## En Termux

```bash
export BRIDGE_SERVER_URL='https://tu-url-ngrok'
export BRIDGE_API_TOKEN='tu-token'
```

Prueba:

```bash
bridge status
```

## Nota

En plan gratis, la URL cambia cuando reinicias ngrok.
