# ✅ Probar que Ollama Funciona

## Configuración Actual

- ✅ Ollama instalado: versión 0.15.6
- ✅ Modelo codellama descargado
- ✅ Configuración guardada en .env

## Próximos Pasos

### 1. Verificar Configuración

```powershell
# Verificar variables en .env
Get-Content .env | Select-String -Pattern "AI_PROVIDER|OLLAMA"

# Deberías ver:
# AI_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=codellama
```

### 2. Verificar que Ollama Está Corriendo

```powershell
# Ver modelos instalados
ollama list

# Deberías ver codellama en la lista
```

### 3. Probar Ollama Directamente

```powershell
# Probar que Ollama responde
ollama run codellama "Escribe una función Python que sume dos números"
```

### 4. Reiniciar el Servidor

**IMPORTANTE:** Debes reiniciar el servidor para que use Ollama:

```powershell
# Detén el servidor actual (Ctrl+C en la terminal donde corre)
# Luego reinicia:
python start_server.py
```

### 5. Probar desde Termux

```bash
# Limpiar el archivo con error primero
rm suma.py

# Probar generar código
cursor query "Crea una función que sume dos números" --write suma.py

# Ver el código generado
cat suma.py
```

## Si No Funciona

### Error: "No se pudo conectar con Ollama"
```powershell
# Iniciar Ollama manualmente
ollama serve

# Dejar corriendo en otra terminal
```

### Error: "Model not found"
```powershell
# Descargar el modelo
ollama pull codellama
```

### Muy Lento
- Es normal la primera vez (carga el modelo)
- Las siguientes consultas serán más rápidas
- Si es muy lento, prueba con un modelo más pequeño: `ollama pull mistral`

## Ventajas de Ollama

- ✅ 100% Gratis
- ✅ Sin límites
- ✅ Privado (todo local)
- ✅ Funciona offline

¡Ya está todo configurado! Solo reinicia el servidor y prueba.
