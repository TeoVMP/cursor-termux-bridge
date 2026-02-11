# 🚀 Guía Rápida: Configurar Ollama (Gratis)

## Paso 1: Instalar Ollama

### Windows:
```powershell
# Opción 1: Descargar desde web
# Ve a: https://ollama.ai/download

# Opción 2: Con winget
winget install Ollama.Ollama
```

### Verificar instalación:
```bash
ollama --version
```

## Paso 2: Descargar Modelo de Código

```bash
# Opción 1: CodeLlama (Recomendado para código)
ollama pull codellama

# Opción 2: DeepSeek Coder (Muy bueno)
ollama pull deepseek-coder

# Opción 3: Llama 3.2 (General, rápido)
ollama pull llama3.2

# Opción 4: Mistral (Rápido y eficiente)
ollama pull mistral
```

## Paso 3: Configurar en el Proyecto

```powershell
# Ejecuta el script de configuración
.\configurar_ollama.ps1

# O edita .env manualmente:
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama
```

## Paso 4: Verificar que Ollama Está Corriendo

```bash
# Ollama debería iniciarse automáticamente
# Verifica:
ollama list

# Si no está corriendo:
ollama serve
```

## Paso 5: Reiniciar el Servidor

```powershell
# Detén el servidor actual (Ctrl+C)
# Reinicia:
python start_server.py
```

## Paso 6: Probar desde Termux

```bash
cursor query "Crea una función que sume dos números" --write suma.py
```

## Troubleshooting

### Error: "No se pudo conectar con Ollama"
- Verifica que Ollama esté corriendo: `ollama list`
- Si no está, ejecuta: `ollama serve`

### Error: "Model not found"
- Descarga el modelo: `ollama pull codellama`
- Verifica que esté descargado: `ollama list`

### Muy lento
- Usa un modelo más pequeño: `ollama pull mistral` o `ollama pull llama3.2`
- O usa GPU si está disponible

### Modelo no genera buen código
- Prueba con `deepseek-coder`: `ollama pull deepseek-coder`
- O `codellama`: `ollama pull codellama`

## Modelos Recomendados para Código

1. **codellama** ⭐⭐⭐⭐⭐ - Especializado en código
2. **deepseek-coder** ⭐⭐⭐⭐⭐ - Excelente calidad
3. **llama3.2** ⭐⭐⭐⭐ - Bueno y rápido
4. **mistral** ⭐⭐⭐ - Rápido pero menos especializado

## Ventajas de Ollama

- ✅ 100% Gratis
- ✅ Sin límites
- ✅ Privado (todo local)
- ✅ Múltiples modelos
- ✅ Funciona offline

## Desventajas

- ⚠️ Requiere GPU o CPU potente
- ⚠️ Puede ser más lento que APIs pagas
- ⚠️ Calidad depende del modelo elegido
