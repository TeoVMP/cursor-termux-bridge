# 🤖 Integrar con Cursor/IA Real

## Estado Actual

Actualmente el servidor retorna respuestas simuladas. Para obtener respuestas reales de Cursor/IA, necesitas integrar con la API.

## Opciones de Integración

### Opción 1: API de Cursor (Si está disponible)

Si Cursor tiene una API pública, puedes integrarla en `server/bridge_server.py`:

```python
# En server/bridge_server.py, función process_query
async def process_query(request: QueryRequest):
    # ... código existente ...
    
    # TODO: Integrar con Cursor API
    # Ejemplo hipotético:
    # cursor_response = await cursor_api.chat(
    #     messages=history,
    #     model="claude-3"
    # )
    # response_text = cursor_response.content
```

### Opción 2: OpenAI API

Si tienes acceso a OpenAI:

```python
import openai

async def process_query(request: QueryRequest):
    # ... código existente ...
    
    # Preparar mensajes para OpenAI
    messages = [
        {"role": "system", "content": "Eres un asistente de programación."}
    ]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": request.query})
    
    # Llamar a OpenAI
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    
    response_text = response.choices[0].message.content
```

### Opción 3: Anthropic Claude API

```python
import anthropic

async def process_query(request: QueryRequest):
    # ... código existente ...
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Preparar mensajes
    messages = []
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Llamar a Claude
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=messages
    )
    
    response_text = response.content[0].text
```

### Opción 4: Modelo Local (Ollama, LM Studio, etc.)

```python
import requests

async def process_query(request: QueryRequest):
    # ... código existente ...
    
    # Preparar mensajes
    messages = []
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    messages.append({"role": "user", "content": request.query})
    
    # Llamar a modelo local
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama2",
            "messages": messages
        }
    )
    
    response_text = response.json()["message"]["content"]
```

## Pasos para Integrar

1. **Elige una opción** (OpenAI, Anthropic, modelo local, etc.)

2. **Instala la librería necesaria:**
   ```bash
   pip install openai  # Para OpenAI
   # o
   pip install anthropic  # Para Anthropic
   ```

3. **Añade la API key al `.env`:**
   ```
   OPENAI_API_KEY=tu-api-key-aqui
   # o
   ANTHROPIC_API_KEY=tu-api-key-aqui
   ```

4. **Modifica `server/bridge_server.py`:**
   - Encuentra la función `process_query`
   - Reemplaza la respuesta simulada con la llamada real a la API

5. **Reinicia el servidor**

## Ejemplo Completo con OpenAI

```python
# En server/bridge_server.py
import openai
import os

# Al inicio del archivo, después de los imports
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# En la función process_query, reemplaza la parte simulada:
# Obtener historial para contexto
history = session_manager.get_messages(session_id)

# Preparar mensajes para OpenAI
messages = [
    {"role": "system", "content": "Eres un asistente de programación experto. Ayudas a escribir código, debuggear y explicar conceptos."}
]

# Añadir historial
for msg in history[:-1]:  # Todos excepto el último (que es la consulta actual)
    messages.append({
        "role": msg["role"],
        "content": msg["content"]
    })

# Añadir consulta actual
messages.append({
    "role": "user",
    "content": request.query
})

# Llamar a OpenAI
try:
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    response_text = response.choices[0].message.content
except Exception as e:
    response_text = f"Error al conectar con IA: {e}"
```

## Nota Importante

El sistema **ya funciona completamente** para:
- ✅ Gestionar sesiones
- ✅ Mantener contexto
- ✅ Editar archivos
- ✅ Sincronizar cambios

Solo necesitas cambiar la parte de generación de respuestas para usar una IA real en lugar de la respuesta simulada.
