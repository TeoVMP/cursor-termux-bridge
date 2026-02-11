# 📱 Configuración con Hotspot WiFi (Sin Servicios de Terceros)

## Paso 1: Activar Hotspot en tu Teléfono Android

1. Abre **Configuración**
2. Ve a **Red e Internet** → **Hotspot y anclaje**
3. Activa **Hotspot WiFi**
4. Configura una contraseña segura
5. Anota el nombre de la red (SSID)

## Paso 2: Conectar tu Computadora al Hotspot

1. En Windows, busca redes WiFi disponibles
2. Conéctate al hotspot de tu teléfono
3. Ingresa la contraseña

## Paso 3: Obtener IP de tu Computadora

En PowerShell:
```powershell
ipconfig
```

Busca la sección de tu conexión WiFi y encuentra **IPv4 Address**.
Ejemplo: `192.168.43.1` o `192.168.137.1` (depende del teléfono)

## Paso 4: Configurar en Termux

```bash
# Reemplaza con la IP que obtuviste
export CURSOR_SERVER_URL='http://192.168.43.1:8000'
export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'

# Hacer permanente
echo "export CURSOR_SERVER_URL='http://192.168.43.1:8000'" >> ~/.bashrc
echo "export API_TOKEN='XUS0awTsqLmEfhMzPexT8xamfuxC9vARBKG2VAeRDsuHQFJtpwF3Sxmci9ClgvUg'" >> ~/.bashrc
source ~/.bashrc
```

## Paso 5: Verificar

```bash
# Verificar que las variables están configuradas
echo $CURSOR_SERVER_URL
echo $API_TOKEN

# Probar conexión
curl $CURSOR_SERVER_URL/health
# Deberías ver: {"status":"ok"}
```

## Paso 6: Iniciar el Servidor

En tu computadora (conectada al hotspot):
```powershell
.\venv\Scripts\Activate.ps1
python start_server.py
```

## Notas Importantes

- ✅ **Sin servicios de terceros** - Todo funciona localmente
- ✅ **Seguro** - Red privada entre tu teléfono y computadora
- ⚠️ **Consume datos móviles** - Si no estás en WiFi
- ⚠️ **Hotspot debe estar activo** - Para que funcione la conexión

## Troubleshooting

### No se conecta
- Verifica que el hotspot esté activo
- Verifica que la computadora esté conectada al hotspot
- Verifica que el servidor esté corriendo
- Prueba con `ping` desde Termux: `ping 192.168.43.1`

### IP diferente
- Algunos teléfonos usan `192.168.137.1` o `192.168.43.1`
- Ejecuta `ipconfig` en Windows para ver la IP correcta

### Consumo de datos
- Si estás en WiFi, el hotspot puede usar WiFi en lugar de datos móviles
- Verifica la configuración de tu teléfono
