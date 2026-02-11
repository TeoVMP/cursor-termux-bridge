# ⚙️ Configurar .env en el Servidor (Ordenador)

## ⚠️ IMPORTANTE: Se edita en el ORDENADOR, NO en el teléfono

El archivo `.env` está en tu **computadora/servidor**, no en Termux.

## Método 1: Script Automático (Windows PowerShell)

```powershell
# Ejecuta este script (ya tiene tu API key configurada)
.\configurar_openai.ps1
```

## Método 2: Editar Manualmente

1. **Abre el archivo `.env`** en tu ordenador (en la carpeta del proyecto)

2. **Añade o modifica estas líneas:**

```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-tu-api-key-aqui
OPENAI_MODEL=gpt-4o
```

3. **Guarda el archivo**

## Método 3: Desde PowerShell (Línea de Comandos)

```powershell
# Añadir configuración de OpenAI
Add-Content .env "`nAI_PROVIDER=openai"
Add-Content .env "OPENAI_API_KEY=sk-tu-api-key-aqui"
Add-Content .env "OPENAI_MODEL=gpt-4"
```

## Verificar Configuración

```powershell
# Ver las variables de IA configuradas
Get-Content .env | Select-String -Pattern "AI_PROVIDER|OPENAI"
```

Deberías ver:
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4
```

## Instalar Librería de OpenAI

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar OpenAI
pip install openai
```

## Reiniciar el Servidor

Después de configurar, **reinicia el servidor**:

```powershell
# Detén el servidor actual (Ctrl+C)
# Luego inicia de nuevo
python start_server.py
```

## ⚠️ Seguridad

**NUNCA** compartas tu API key públicamente. Si ya la compartiste:
1. Ve a https://platform.openai.com/api-keys
2. Revoca la key actual
3. Crea una nueva
4. Actualiza `.env` con la nueva key

## Probar que Funciona

Desde Termux:
```bash
cursor query "Hola, ¿funcionas con IA real?" 
```

Deberías ver una respuesta real de GPT-4, no la respuesta simulada.
