# 🔍 Diagnóstico de Conexión

## Problema Común: VPN Interfiriendo

Si tienes una VPN activa (como ProtonVPN, NordVPN, etc.), puede interferir con las conexiones locales.

### Solución:
1. **Desconecta la VPN** completamente
2. **Verifica tu IP WiFi** nuevamente
3. **Reintenta la conexión**

## Verificar que el Servidor Está Escuchando Correctamente

El servidor debe estar escuchando en `0.0.0.0:8000` (todas las interfaces), no solo en `127.0.0.1:8000` (localhost).

### Verificar en Windows:
```powershell
netstat -an | findstr ":8000"
```

Deberías ver algo como:
```
TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING
```

Si solo ves `127.0.0.1:8000`, el servidor solo acepta conexiones locales.

## Configuración Correcta del Servidor

Asegúrate de que el servidor esté configurado para escuchar en todas las interfaces:

En `server/bridge_server.py` o `start_server.py`, debe estar:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

NO:
```python
uvicorn.run(app, host="127.0.0.1", port=8000)  # ❌ Solo localhost
```

## Verificar Firewall de Windows

El firewall puede estar bloqueando el puerto 8000:

```powershell
# Ver reglas del firewall
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Python*"}

# Si está bloqueado, permite Python a través del firewall
# O crea una regla manual para el puerto 8000
```

## Pasos de Diagnóstico Completos

1. ✅ **Desconecta VPN**
2. ✅ **Verifica IP WiFi**: `ipconfig` o `Get-NetIPAddress`
3. ✅ **Inicia servidor**: `python start_server.py`
4. ✅ **Verifica que escucha en 0.0.0.0**: `netstat -an | findstr ":8000"`
5. ✅ **Prueba localmente**: `curl http://localhost:8000/health`
6. ✅ **Prueba desde Termux**: `curl http://TU_IP:8000/health`

## Comandos Útiles

### En Windows (PowerShell):
```powershell
# Ver IP WiFi
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*WiFi*"}

# Ver qué está escuchando en puerto 8000
netstat -an | findstr ":8000"

# Probar conexión local
Invoke-WebRequest -Uri http://localhost:8000/health
```

### En Termux:
```bash
# Verificar variables
echo $CURSOR_SERVER_URL
echo $API_TOKEN

# Probar conexión
curl $CURSOR_SERVER_URL/health

# Probar con ping primero
ping TU_IP_AQUI
```
