# 📱 Configuración en Termux

## Paso 1: Obtener el Token del Servidor

El `API_TOKEN` viene del archivo `.env` de tu servidor (computadora).

1. **En tu computadora**, abre el archivo `.env`:
   ```bash
   # Si no existe, cópialo desde el ejemplo
   cp config/env.example .env
   ```

2. **Edita el archivo `.env`** y busca la línea:
   ```
   API_TOKEN=change-me-in-production
   ```

3. **Cambia el token** por uno seguro (puedes generar uno aleatorio):
   ```
   API_TOKEN=mi-token-super-secreto-12345
   ```
   
   O genera uno aleatorio:
   ```bash
   # En Linux/Mac
   openssl rand -hex 32
   
   # En Windows PowerShell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
   ```

4. **Guarda el archivo** y reinicia el servidor si está corriendo.

## Paso 2: Obtener la URL del Servidor

### Opción A: Misma red local (WiFi)

1. **En tu computadora**, encuentra tu IP:
   ```bash
   # Windows PowerShell
   ipconfig
   # Busca "IPv4 Address" (ej: 192.168.1.100)
   
   # Linux/Mac
   ifconfig
   # o
   ip addr show
   ```

2. **La URL será**: `http://TU_IP:8000`
   Ejemplo: `http://192.168.1.100:8000`

### Opción B: Con ngrok (acceso remoto)

1. **Instala ngrok** en tu computadora: https://ngrok.com/

2. **Ejecuta**:
   ```bash
   ngrok http 8000
   ```

3. **Copia la URL HTTPS** que te da (ej: `https://abc123.ngrok.io`)

4. **La URL será**: `https://abc123.ngrok.io`

## Paso 3: Configurar en Termux

### Método 1: Temporal (solo esta sesión)

```bash
export CURSOR_SERVER_URL='http://192.168.1.100:8000'
export API_TOKEN='mi-token-super-secreto-12345'
```

### Método 2: Permanente (recomendado)

Edita el archivo `~/.bashrc`:

```bash
# Abrir editor
nano ~/.bashrc

# Añade estas líneas al final (reemplaza con tus valores):
export CURSOR_SERVER_URL='http://192.168.1.100:8000'
export API_TOKEN='mi-token-super-secreto-12345'

# Guarda (Ctrl+O, Enter, Ctrl+X)
```

O usa echo para añadirlo automáticamente:

```bash
echo "export CURSOR_SERVER_URL='http://192.168.1.100:8000'" >> ~/.bashrc
echo "export API_TOKEN='mi-token-super-secreto-12345'" >> ~/.bashrc
source ~/.bashrc
```

## Paso 4: Verificar Configuración

```bash
# Verificar que las variables están configuradas
echo $CURSOR_SERVER_URL
echo $API_TOKEN

# Probar conexión con el servidor
curl $CURSOR_SERVER_URL/health
# Deberías ver: {"status":"ok"}
```

## Ejemplo Completo

```bash
# 1. Configurar variables (reemplaza con tus valores)
export CURSOR_SERVER_URL='http://192.168.1.100:8000'
export API_TOKEN='abc123xyz789'

# 2. Hacer permanente
echo "export CURSOR_SERVER_URL='http://192.168.1.100:8000'" >> ~/.bashrc
echo "export API_TOKEN='abc123xyz789'" >> ~/.bashrc

# 3. Recargar configuración
source ~/.bashrc

# 4. Verificar
echo $CURSOR_SERVER_URL
echo $API_TOKEN
```

## Troubleshooting

### El token no funciona
- Verifica que el token en `.env` del servidor sea el mismo
- Reinicia el servidor después de cambiar el token
- Verifica que no haya espacios extra: `API_TOKEN=token` (no `API_TOKEN= token`)

### No se conecta al servidor
- Verifica que el servidor esté corriendo: `curl http://localhost:8000/health`
- Verifica que la IP sea correcta
- Verifica que el firewall permita conexiones en el puerto 8000
- Si usas ngrok, verifica que la URL sea HTTPS (no HTTP)

### Las variables no persisten
- Verifica que `~/.bashrc` tenga las líneas correctas
- Asegúrate de usar `source ~/.bashrc` después de editarlo
- En algunos casos, usa `~/.bash_profile` en lugar de `~/.bashrc`
