# 🆓 Modelos Gratuitos y Sin Límites

## Opción 1: Ollama (Recomendado - 100% Gratis)

**Ventajas:**
- ✅ Completamente gratis
- ✅ Sin límites
- ✅ Funciona localmente (privado)
- ✅ Múltiples modelos disponibles

**Desventajas:**
- ⚠️ Requiere GPU o CPU potente
- ⚠️ Calidad puede variar según el modelo

### Instalación:

1. **Descarga Ollama:**
   - Windows: https://ollama.ai/download
   - O desde terminal: `winget install Ollama.Ollama`

2. **Instala un modelo de código:**
   ```bash
   # Modelos recomendados para código:
   ollama pull codellama        # Especializado en código
   ollama pull deepseek-coder   # Muy bueno para código
   ollama pull llama3.2         # Modelo general bueno
   ollama pull mistral          # Rápido y eficiente
   ```

3. **Configura en `.env`:**
   ```bash
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=codellama
   ```

4. **Reinicia el servidor**

## Opción 2: LM Studio (Gratis, con Interfaz Gráfica)

**Ventajas:**
- ✅ Interfaz gráfica amigable
- ✅ Fácil de usar
- ✅ Múltiples modelos

**Desventajas:**
- ⚠️ Requiere descargar modelos manualmente
- ⚠️ Requiere GPU/CPU potente

### Instalación:

1. **Descarga LM Studio:** https://lmstudio.ai/
2. **Descarga un modelo** desde la interfaz
3. **Inicia el servidor local** en LM Studio
4. **Configura en `.env`:**
   ```bash
   AI_PROVIDER=lmstudio
   LMSTUDIO_BASE_URL=http://localhost:1234
   LMSTUDIO_MODEL=local-model
   ```

## Opción 3: Hugging Face Inference API (Gratis con límites)

Algunos modelos tienen API gratuita con límites generosos.

## Opción 4: Groq (Gratis, Muy Rápido)

Groq ofrece API gratuita con límites generosos y es muy rápido.

### Configuración Groq:

1. **Crea cuenta:** https://console.groq.com/
2. **Obtén API key**
3. **Configura en `.env`:**
   ```bash
   AI_PROVIDER=groq
   GROQ_API_KEY=tu-api-key
   GROQ_MODEL=llama-3.1-70b-versatile
   ```

## 🎯 Recomendación: Ollama con CodeLlama

Para desarrollo de código, **Ollama + CodeLlama** es la mejor opción gratuita:

```bash
# Instalar Ollama
# Luego:
ollama pull codellama

# Configurar .env:
AI_PROVIDER=ollama
OLLAMA_MODEL=codellama
```

## 📊 Comparación de Modelos Gratuitos

| Modelo | Calidad Código | Velocidad | Requisitos |
|--------|---------------|-----------|------------|
| CodeLlama (Ollama) | ⭐⭐⭐⭐ | ⭐⭐⭐ | GPU recomendada |
| DeepSeek Coder | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | GPU recomendada |
| Llama 3.2 | ⭐⭐⭐ | ⭐⭐⭐⭐ | CPU suficiente |
| Mistral | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | CPU suficiente |

## 🚀 Setup Rápido con Ollama

```powershell
# 1. Instalar Ollama (si no está)
winget install Ollama.Ollama

# 2. Reiniciar terminal, luego:
ollama pull codellama

# 3. Configurar .env
.\configurar_ollama.ps1

# 4. Reiniciar servidor
python start_server.py
```
