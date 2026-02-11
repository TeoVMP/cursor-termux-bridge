# Cursor-Termux Bridge

Sistema que permite escribir código en Termux desde tu teléfono Pixel con GrapheneOS, hacer consultas a Cursor/IA, y sincronizar archivos bidireccionalmente entre el teléfono y tu computadora.

## Características

- ✅ **Consultas a Cursor/IA** desde Termux con contexto persistente
- ✅ **Edición de código** con nano integrado
- ✅ **Sincronización automática** de archivos después de editar
- ✅ **Gestión de sesiones** con historial completo de conversaciones
- ✅ **Sincronización Git** bidireccional
- ✅ **Backup automático** antes de editar archivos

## Arquitectura

El sistema consta de tres componentes principales:

1. **Servidor Bridge** (en tu computadora): API REST que actúa como intermediario
2. **Cliente Termux** (en tu Pixel): CLI para interactuar con el servidor
3. **Sistema de Sincronización**: Git para cambios bidireccionales

## Instalación

### En la Computadora (Servidor)

1. Clona o descarga este repositorio
2. Ejecuta el script de instalación:
   ```bash
   bash config/setup_server.sh
   ```
3. Configura las variables de entorno en `.env`:
   ```bash
   cp config/.env.example .env
   # Edita .env con tus configuraciones
   ```
4. Inicia el servidor:
   ```bash
   source venv/bin/activate  # o venv/Scripts/activate en Windows
   python start_server.py
   # O directamente: python server/bridge_server.py
   ```

### En Termux (Pixel)

1. Ejecuta el script de instalación:
   ```bash
   bash config/setup_termux.sh
   ```
2. Copia el cliente a Termux (desde tu computadora):
   ```bash
   scp -r termux/ usuario@ip-del-telefono:/data/data/com.termux/files/home/
   ```
   O descarga directamente en Termux si tienes acceso a git.
3. Configura las variables de entorno:
   ```bash
   export CURSOR_SERVER_URL='http://tu-servidor:8000'
   export API_TOKEN='tu-token'
   ```
   Añade estas líneas a `~/.bashrc` para que persistan.
4. Haz el cliente ejecutable:
   ```bash
   chmod +x termux/cursor_client.py
   ```
5. Crea un alias (opcional):
   ```bash
   echo "alias cursor='python3 ~/termux/cursor_client.py'" >> ~/.bashrc
   source ~/.bashrc
   ```

## Configuración de Acceso Remoto

Para acceder al servidor desde tu teléfono, necesitas exponerlo de forma segura:

### Opción 1: ngrok (Recomendado para pruebas)
```bash
ngrok http 8000
# Usa la URL HTTPS proporcionada en CURSOR_SERVER_URL
```

### Opción 2: Tailscale (Recomendado para producción)
```bash
# En ambos dispositivos
tailscale up
# Usa la IP de Tailscale en CURSOR_SERVER_URL
```

### Opción 3: SSH Tunnel
```bash
ssh -R 8000:localhost:8000 usuario@servidor
```

## Uso

### Hacer Consultas

```bash
# Primera consulta (crea sesión automáticamente)
cursor query "¿cómo creo una función en Python?"

# Continuar la conversación (usa la misma sesión)
cursor query "ahora hazla async"

# Crear nueva sesión
cursor query "nueva pregunta" --new-session
```

### Editar Archivos

```bash
# Editar un archivo (sincroniza automáticamente)
cursor edit archivo.py

# Editar múltiples archivos
cursor edit file1.py file2.py

# Editar sin sincronizar automáticamente
cursor edit archivo.py --no-sync
```

### Gestionar Sesiones

```bash
# Listar todas las sesiones
cursor sessions

# Ver historial de la sesión actual
cursor history

# Cambiar a otra sesión
cursor session <session_id>
```

### Otros Comandos

```bash
# Listar archivos del proyecto
cursor list

# Ver contenido de un archivo
cursor open archivo.py

# Sincronizar manualmente
cursor sync
```

## Estructura del Proyecto

```
.
├── server/
│   ├── bridge_server.py      # Servidor FastAPI
│   └── session_manager.py    # Gestor de sesiones
├── termux/
│   ├── cursor_client.py      # Cliente CLI
│   └── nano_wrapper.py       # Wrapper para nano
├── sync/
│   └── git_sync.py           # Utilidades de sincronización Git
├── config/
│   ├── setup_termux.sh       # Script de instalación para Termux
│   ├── setup_server.sh       # Script de instalación para servidor
│   ├── .env.example          # Plantilla de configuración
│   └── nanorc.example        # Configuración de nano
├── requirements.txt          # Dependencias Python
└── README.md                 # Este archivo
```

## Seguridad

- **Autenticación**: Usa tokens API seguros (cambia el valor por defecto)
- **HTTPS**: Usa ngrok con TLS o tailscale para conexiones seguras
- **Validación**: El servidor valida rutas de archivos para prevenir acceso no autorizado
- **Rate Limiting**: Considera añadir rate limiting en producción

## Desarrollo

### Ejecutar el servidor en modo desarrollo

```bash
uvicorn server.bridge_server:app --reload --host 0.0.0.0 --port 8000
```

### Verificar salud del servidor

```bash
curl http://localhost:8000/health
```

## Integración con Cursor/IA

Actualmente, el endpoint `/query` retorna respuestas simuladas. Para integrar con Cursor/IA real:

1. Investiga la API de Cursor (si está disponible)
2. O integra con OpenAI/Anthropic directamente
3. Modifica el método `process_query` en `server/bridge_server.py`

## Troubleshooting

### El cliente no se conecta al servidor
- Verifica que el servidor esté corriendo
- Verifica la URL en `CURSOR_SERVER_URL`
- Verifica que el firewall permita conexiones en el puerto

### nano no se abre
- Verifica que nano esté instalado: `pkg install nano`
- Verifica permisos: `chmod +x termux/cursor_client.py`

### Los archivos no se sincronizan
- Verifica que Git esté configurado correctamente
- Verifica permisos de escritura en el workspace
- Revisa los logs del servidor

## Licencia

Este proyecto es de código abierto. Úsalo y modifícalo según tus necesidades.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## Soporte

Si encuentras problemas o tienes preguntas, por favor abre un issue en el repositorio.
