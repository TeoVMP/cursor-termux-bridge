# Setup remoto con Tailscale

## En PC y Android

1. Instala Tailscale en ambos dispositivos.
2. Inicia sesion con la misma cuenta.
3. Verifica la IP de la PC:

```powershell
tailscale ip
```

## En Termux

```bash
export BRIDGE_SERVER_URL='http://100.x.y.z:8765'
export BRIDGE_API_TOKEN='tu-token'
```

Prueba:

```bash
bridge status
```

Si funciona, guarda variables en `~/.bashrc`.
