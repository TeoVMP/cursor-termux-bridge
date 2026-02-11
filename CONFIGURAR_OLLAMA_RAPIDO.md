# 🚀 Configurar Ollama Rápido (Gratis)

## Tu Problema Actual

- ❌ Cuota de OpenAI excedida
- ❌ El sistema necesita una IA funcionando

## Solución: Ollama (100% Gratis)

### Paso 1: Instalar Ollama en tu Ordenador

**Windows:**
```powershell
# Opción 1: Descargar
# Ve a: https://ollama.ai/download

# Opción 2: Con winget
winget install Ollama.Ollama
```

### Paso 2: Descargar Modelo de Código

```bash
# Abre PowerShell o CMD y ejecuta:
ollama pull codellama

# Esto descargará ~4GB, puede tardar unos minutos
```

### Paso 3: Verificar que Ollama Funciona

```bash
# Probar que Ollama responde
ollama list

# Deberías ver codellama en la lista
```

### Paso 4: Configurar el Proyecto

**En tu ordenador (PowerShell):**
```powershell
# Ejecuta el script de configuración
.\configurar_ollama.ps1

# O edita .env manualmente:
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama
```

### Paso 5: Reiniciar el Servidor

```powershell
# Detén el servidor actual (Ctrl+C)
# Reinicia:
python start_server.py
```

### Paso 6: Probar desde Termux

```bash
cursor query "Crea una función que sume dos números" --write suma.py
```

## Modelos Recomendados

### Para Código (Mejor Calidad):
```bash
ollama pull codellama        # ~4GB - Especializado en código
ollama pull deepseek-coder   # ~4GB - Muy bueno para código
```

### Para Rápido (Menos Calidad):
```bash
ollama pull mistral          # ~4GB - Rápido y eficiente
ollama pull llama3.2         # ~2GB - Pequeño y rápido
```

## Troubleshooting

### Ollama no responde
```bash
# Iniciar Ollama manualmente
ollama serve

# Dejar corriendo en otra terminal
```

### Modelo no encontrado
```bash
# Ver modelos instalados
ollama list

# Si no está, descargar:
ollama pull codellama
```

### Muy lento
- Usa un modelo más pequeño: `ollama pull mistral`
- O verifica que tengas GPU disponible

### Error de conexión
- Verifica que Ollama esté corriendo: `ollama list`
- Verifica la URL en `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

## Ventajas de Ollama

- ✅ 100% Gratis
- ✅ Sin límites
- ✅ Privado (todo local)
- ✅ Funciona offline
- ✅ Múltiples modelos

## Después de Configurar

Una vez configurado, puedes usar el sistema normalmente:

```bash
# Generar código
cursor query "Crea una función..." --write archivo.py

# Integrar código
cursor query "Añade validación" --write archivo.py

# Todo funciona igual, pero gratis!
```
