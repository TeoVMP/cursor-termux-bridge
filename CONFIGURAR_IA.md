# 🤖 Configurar IA para Escribir Código en Tiempo Real

## Opciones Disponibles

### 1. OpenAI (GPT-4, GPT-3.5) - Recomendado

**Ventajas:**
- ✅ Muy buena calidad de código
- ✅ Rápido
- ✅ Fácil de configurar

**Configuración:**

1. Obtén tu API key: https://platform.openai.com/api-keys
2. Instala la librería:
   ```bash
   pip install openai
   ```
3. Añade al `.env`:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-tu-api-key-aqui
   OPENAI_MODEL=gpt-4  # o gpt-3.5-turbo para más barato
   ```

### 2. Anthropic Claude (Opus, Sonnet)

**Ventajas:**
- ✅ Excelente calidad
- ✅ Muy bueno para código

**Configuración:**

1. Obtén tu API key: https://console.anthropic.com/
2. Instala la librería:
   ```bash
   pip install anthropic
   ```
3. Añade al `.env`:
   ```
   AI_PROVIDER=anthropic
   ANTHROPIC_API_KEY=tu-api-key-aqui
   ANTHROPIC_MODEL=claude-3-opus-20240229
   ```

### 3. Ollama (Modelo Local - Gratis)

**Ventajas:**
- ✅ Completamente gratis
- ✅ Privado (todo local)
- ✅ Sin límites

**Desventajas:**
- ⚠️ Requiere GPU potente o CPU rápida
- ⚠️ Calidad puede variar según el modelo

**Configuración:**

1. Instala Ollama: https://ollama.ai/
2. Descarga un modelo:
   ```bash
   ollama pull llama2
   # o
   ollama pull codellama
   ```
3. Añade al `.env`:
   ```
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

### 4. LM Studio (Modelo Local - Gratis)

Similar a Ollama pero con interfaz gráfica.

**Configuración:**

1. Instala LM Studio: https://lmstudio.ai/
2. Descarga un modelo desde la interfaz
3. Inicia el servidor local en LM Studio
4. Añade al `.env`:
   ```
   AI_PROVIDER=lmstudio
   LMSTUDIO_BASE_URL=http://localhost:1234
   LMSTUDIO_MODEL=local-model
   ```

## Uso Básico

### Consulta Normal
```bash
cursor query "¿Cómo creo una función en Python?"
```

### Generar Código y Escribirlo en Archivo
```bash
cursor query "Crea una función que sume dos números" --write suma.py
```

La IA generará el código y lo escribirá automáticamente en `suma.py`.

### Ejemplos de Uso

```bash
# Crear un script Python completo
cursor query "Crea un script que lea un archivo JSON y muestre su contenido" --write leer_json.py

# Crear una clase
cursor query "Crea una clase Usuario con nombre, email y método para mostrar info" --write usuario.py

# Modificar código existente (primero pregunta qué hacer)
cursor query "Añade validación de email a la clase Usuario" --write usuario.py

# Crear múltiples archivos (hazlo uno por uno)
cursor query "Crea un archivo HTML con un formulario de contacto" --write contacto.html
cursor query "Crea el CSS para el formulario" --write estilo.css
```

## Verificar Configuración

```bash
# En el servidor, verifica que las variables están configuradas
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('AI Provider:', os.getenv('AI_PROVIDER')); print('API Key configurada:', 'Sí' if os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY') else 'No')"
```

## Troubleshooting

### Error: "AI_PROVIDER no configurado"
- Verifica que `.env` tenga `AI_PROVIDER=openai` (o el proveedor que uses)
- Reinicia el servidor después de cambiar `.env`

### Error: "API key no configurada"
- Verifica que la API key esté en `.env`
- Asegúrate de que el nombre de la variable sea correcto:
  - `OPENAI_API_KEY` para OpenAI
  - `ANTHROPIC_API_KEY` para Anthropic

### Error: "No se pudo generar código"
- Verifica que la API key sea válida
- Verifica tu balance/créditos en la plataforma
- Si usas modelo local, verifica que esté corriendo

### El código no se escribe en el archivo
- Verifica permisos de escritura en el workspace
- Verifica que la ruta del archivo sea correcta
- Revisa los logs del servidor para ver errores

## Costos Aproximados

- **OpenAI GPT-4**: ~$0.03 por consulta (depende de tokens)
- **OpenAI GPT-3.5**: ~$0.002 por consulta (más barato)
- **Anthropic Claude Opus**: ~$0.015 por 1K tokens
- **Ollama/LM Studio**: Gratis (pero requiere hardware)

## Recomendación

Para empezar rápido:
1. Usa **OpenAI GPT-3.5-turbo** (barato y rápido)
2. O usa **Ollama** si tienes buena GPU (gratis)

Para mejor calidad:
- **OpenAI GPT-4** o **Anthropic Claude Opus**
