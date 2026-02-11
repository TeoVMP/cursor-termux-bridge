# 🤖 Modelos de OpenAI Disponibles

## Modelos Recomendados

### 1. gpt-4-turbo (Recomendado)
- ✅ Mejor relación calidad/precio
- ✅ Más rápido que gpt-4
- ✅ Muy buena calidad de código
- **Uso:** `OPENAI_MODEL=gpt-4-turbo`

### 2. gpt-3.5-turbo (Más Barato)
- ✅ Muy rápido
- ✅ Más económico
- ✅ Buena calidad para código simple
- **Uso:** `OPENAI_MODEL=gpt-3.5-turbo`

### 3. gpt-4 (Si tienes acceso)
- ✅ Máxima calidad
- ⚠️ Más caro
- ⚠️ Más lento
- ⚠️ Puede requerir acceso especial
- **Uso:** `OPENAI_MODEL=gpt-4`

## Cambiar Modelo

### Método 1: Script Automático
```powershell
# Cambiar a gpt-4-turbo
.\cambiar_modelo.ps1 gpt-4-turbo

# Cambiar a gpt-3.5-turbo (más barato)
.\cambiar_modelo.ps1 gpt-3.5-turbo
```

### Método 2: Editar .env Manualmente
Abre `.env` y cambia:
```bash
OPENAI_MODEL=gpt-4-turbo
```

### Método 3: PowerShell
```powershell
(Get-Content .env) -replace 'OPENAI_MODEL=.*', 'OPENAI_MODEL=gpt-4-turbo' | Set-Content .env
```

## Verificar Modelo Actual

```powershell
Get-Content .env | Select-String "OPENAI_MODEL"
```

## Después de Cambiar

**IMPORTANTE:** Reinicia el servidor:
```powershell
# Detén el servidor (Ctrl+C)
# Reinicia:
python start_server.py
```

## Costos Aproximados

- **gpt-4-turbo**: ~$0.01 por 1K tokens (entrada), ~$0.03 por 1K tokens (salida)
- **gpt-3.5-turbo**: ~$0.0005 por 1K tokens (entrada), ~$0.0015 por 1K tokens (salida)
- **gpt-4**: ~$0.03 por 1K tokens (entrada), ~$0.06 por 1K tokens (salida)

## Recomendación

Para desarrollo de código:
- **gpt-4-turbo** - Mejor opción (buena calidad, precio razonable)
- **gpt-3.5-turbo** - Si quieres ahorrar dinero (suficiente para código simple)
