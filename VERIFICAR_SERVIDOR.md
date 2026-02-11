# 🔍 Verificar que el Servidor Está Funcionando

## Problema: Timeout

El error de timeout puede ser porque:
1. El servidor no está corriendo
2. Ollama está tardando mucho (normal)
3. Problema de conexión

## Verificación Paso a Paso

### 1. Verificar que el Servidor Está Corriendo

**En tu ordenador (PowerShell):**
```powershell
# Ver procesos Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Verificar puerto 8000
Test-NetConnection -ComputerName localhost -Port 8000
```

**Si el servidor NO está corriendo:**
```powershell
# Iniciar servidor
python start_server.py

# Deberías ver:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Verificar que Ollama Está Corriendo

```powershell
# Ver modelos instalados
ollama list

# Probar Ollama directamente
ollama run codellama "Escribe una función Python simple que sume dos números"
```

**Si Ollama no responde:**
```powershell
# Iniciar Ollama manualmente (en otra terminal)
ollama serve

# Dejar corriendo
```

### 3. Verificar Configuración

```powershell
# Verificar .env
Get-Content .env | Select-String -Pattern "AI_PROVIDER|OLLAMA"

# Debería mostrar:
# AI_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=codellama
```

### 4. Probar Conexión Básica

**Desde Termux:**
```bash
# Probar conexión básica (sin IA)
curl $CURSOR_SERVER_URL/health

# Deberías ver: {"status":"ok"}
```

### 5. Probar con Timeout Aumentado

**Actualiza el código en Termux:**
```bash
git pull
```

**Luego prueba:**
```bash
# Ahora con timeout de 120 segundos
cursor query "Crea una función que sume dos números" --write suma.py
```

## Si Sigue Fallando

### Ver Logs del Servidor

En la terminal donde corre el servidor, deberías ver logs. Si hay errores, aparecerán ahí.

### Probar Ollama Directamente

```powershell
# En tu ordenador
ollama run codellama "Escribe una función Python que sume dos números"
```

Si esto funciona, Ollama está bien. El problema puede ser:
- El servidor no está usando Ollama correctamente
- Timeout aún muy corto
- Problema de red

### Usar Modelo Más Rápido

```powershell
# Cambiar a mistral (más rápido)
.\cambiar_modelo.ps1 mistral

# Reiniciar servidor
```

## Solución Temporal: Aumentar Timeout Manualmente

Si necesitas más tiempo, edita `termux/cursor_client.py`:

```python
# Línea ~44, cambiar:
timeout_value = kwargs.pop('timeout', 300)  # 5 minutos
```

## Notas Importantes

- ✅ Timeouts aumentados a 120s (cliente) y 180s (servidor)
- ⚠️ Primera consulta con Ollama puede tardar 1-2 minutos
- ⚠️ Consultas siguientes serán más rápidas
- ⚠️ Es normal que Ollama sea más lento que APIs pagas
