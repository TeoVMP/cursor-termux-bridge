# 🧪 Guía de Pruebas - Cursor-Termux Bridge

## ✅ Paso 1: Verificar Conexión (YA COMPLETADO)
```bash
curl $CURSOR_SERVER_URL/health
# Deberías ver: {"status":"ok"}
```

## 📝 Paso 2: Probar Hacer una Consulta

```bash
# Hacer tu primera consulta (creará una sesión automáticamente)
cursor query "Hola, ¿puedes ayudarme con Python?"

# Deberías ver una respuesta del servidor
```

## 📋 Paso 3: Ver Sesiones Creadas

```bash
# Listar todas las sesiones
cursor sessions

# Ver el historial de la sesión actual
cursor history
```

## 📁 Paso 4: Listar Archivos del Proyecto

```bash
# Ver qué archivos hay en el workspace del servidor
cursor list
```

## 📝 Paso 5: Crear/Editar un Archivo

```bash
# Crear un archivo de prueba
cursor edit test.py

# Se abrirá nano, escribe algo como:
# print("Hola desde Termux!")
# Guarda con Ctrl+O, Enter, Ctrl+X

# El archivo se sincronizará automáticamente
```

## 👀 Paso 6: Ver Contenido de un Archivo

```bash
# Ver el contenido sin editar
cursor open test.py
```

## 🔄 Paso 7: Probar Sincronización

```bash
# Sincronizar manualmente
cursor sync
```

## 🔍 Paso 8: Probar Múltiples Consultas (Contexto)

```bash
# Primera consulta
cursor query "Crea una función que sume dos números"

# Segunda consulta (debería recordar el contexto)
cursor query "Ahora hazla async"

# Ver historial completo
cursor history
```

## 🎯 Pruebas Avanzadas

### Probar con Archivo Existente
```bash
# Editar un archivo que ya existe en el servidor
cursor edit README.md
```

### Probar Múltiples Archivos
```bash
# Editar varios archivos seguidos
cursor edit file1.py file2.py
```

### Cambiar de Sesión
```bash
# Ver sesiones disponibles
cursor sessions

# Cambiar a otra sesión
cursor session <session_id>
```

## 🐛 Si Algo No Funciona

### El comando `cursor` no se encuentra
```bash
# Verificar que el alias está configurado
alias cursor

# Si no está, añádelo:
echo "alias cursor='python3 ~/software-tools/cursor-termux-bridge/termux/cursor_client.py'" >> ~/.bashrc
source ~/.bashrc
```

### Error de permisos
```bash
# Hacer ejecutable
chmod +x termux/cursor_client.py
```

### Error de conexión
```bash
# Verificar variables
echo $CURSOR_SERVER_URL
echo $API_TOKEN

# Probar conexión básica
curl $CURSOR_SERVER_URL/health
```

## ✅ Checklist de Pruebas

- [x] Conexión al servidor funciona
- [ ] Hacer una consulta funciona
- [ ] Ver sesiones funciona
- [ ] Ver historial funciona
- [ ] Listar archivos funciona
- [ ] Crear archivo nuevo funciona
- [ ] Editar archivo funciona
- [ ] Ver archivo funciona
- [ ] Sincronización funciona
- [ ] Contexto entre consultas funciona
