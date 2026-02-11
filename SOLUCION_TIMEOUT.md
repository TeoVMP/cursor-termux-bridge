# ⏱️ Solución: Error de Timeout

## Problema

Ollama puede tardar más de 30 segundos en generar código, especialmente:
- Primera consulta (carga el modelo)
- Código complejo
- Integración inteligente con código existente

## Solución Aplicada

Se aumentaron los timeouts:
- **Cliente Termux**: 30s → 120s (2 minutos)
- **Servidor Ollama**: 120s → 180s (3 minutos)

## Verificar que el Servidor Está Corriendo

En tu ordenador, verifica:

```powershell
# Verificar que el servidor está corriendo
# Deberías ver algo como:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

Si no está corriendo:
```powershell
python start_server.py
```

## Verificar que Ollama Está Corriendo

```powershell
# Verificar modelos
ollama list

# Probar Ollama directamente
ollama run codellama "Escribe una función Python simple"
```

Si Ollama no responde:
```powershell
# Iniciar Ollama manualmente (en otra terminal)
ollama serve
```

## Probar de Nuevo

Desde Termux:
```bash
# Ahora con timeout aumentado
cursor query "Crea una función que sume dos números" --write suma.py
```

## Si Sigue Siendo Muy Lento

### Opción 1: Usar Modelo Más Pequeño
```powershell
# Cambiar a mistral (más rápido)
.\cambiar_modelo.ps1 mistral

# O llama3.2 (más pequeño)
.\cambiar_modelo.ps1 llama3.2
```

### Opción 2: Verificar GPU
Ollama funciona mejor con GPU. Si tienes GPU NVIDIA:
```powershell
# Ollama debería detectarla automáticamente
# Verifica en los logs cuando ejecutas ollama run
```

### Opción 3: Consultas Más Simples
Para código simple, Ollama debería responder rápido. Si es código complejo, es normal que tarde más.

## Notas

- ✅ Timeouts aumentados
- ✅ Primera consulta puede tardar más (carga modelo)
- ✅ Consultas siguientes serán más rápidas
- ✅ Es normal que Ollama sea más lento que APIs pagas
