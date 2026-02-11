# Guía de Inicio Rápido

## Paso 1: Configurar el Servidor (Computadora)

```bash
# 1. Instalar dependencias
bash config/setup_server.sh

# 2. Configurar variables de entorno
cp config/env.example .env
# Edita .env con tus configuraciones

# 3. Iniciar servidor
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate      # Windows

python server/bridge_server.py
```

## Paso 2: Exponer el Servidor (Opcional pero Recomendado)

### Con ngrok:
```bash
ngrok http 8000
# Copia la URL HTTPS (ej: https://abc123.ngrok.io)
```

### Con Tailscale:
```bash
tailscale up
# Usa la IP de Tailscale
```

## Paso 3: Configurar Termux (Pixel)

```bash
# 1. Instalar dependencias
bash config/setup_termux.sh

# 2. Copiar cliente a Termux (desde computadora)
scp -r termux/ usuario@ip:/data/data/com.termux/files/home/

# 3. Configurar variables de entorno en Termux
export CURSOR_SERVER_URL='http://tu-servidor:8000'  # o URL de ngrok
export API_TOKEN='tu-token-del-env'

# Añadir a ~/.bashrc para persistencia
echo "export CURSOR_SERVER_URL='http://tu-servidor:8000'" >> ~/.bashrc
echo "export API_TOKEN='tu-token'" >> ~/.bashrc

# 4. Hacer ejecutable y crear alias
chmod +x termux/cursor_client.py
echo "alias cursor='python3 ~/termux/cursor_client.py'" >> ~/.bashrc
source ~/.bashrc
```

## Paso 4: Usar el Sistema

```bash
# Hacer una consulta
cursor query "¿cómo creo una función en Python?"

# Editar un archivo
cursor edit archivo.py

# Ver historial
cursor history

# Listar archivos
cursor list
```

## Solución de Problemas Comunes

### Error de conexión
- Verifica que el servidor esté corriendo
- Verifica la URL en `CURSOR_SERVER_URL`
- Verifica el firewall

### nano no funciona
```bash
pkg install nano
```

### Permisos denegados
```bash
chmod +x termux/cursor_client.py
```
