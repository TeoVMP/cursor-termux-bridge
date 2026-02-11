# 🎯 Modelos Recomendados para Código

Basado en los modelos disponibles en tu cuenta, aquí están las mejores opciones:

## 🏆 Mejor Opción: GPT-4o

```bash
OPENAI_MODEL=gpt-4o
```

**Ventajas:**
- ✅ El modelo más avanzado disponible
- ✅ Excelente para código complejo
- ✅ Muy rápido
- ✅ Ya configurado en tu sistema

**Cambiar:**
```powershell
.\cambiar_modelo.ps1 gpt-4o
```

## 💰 Opción Económica: GPT-3.5-turbo

```bash
OPENAI_MODEL=gpt-3.5-turbo
```

**Ventajas:**
- ✅ Muy económico
- ✅ Rápido
- ✅ Suficiente para código simple

**Cambiar:**
```powershell
.\cambiar_modelo.ps1 gpt-3.5-turbo
```

## 📋 Otros Modelos Disponibles

### GPT-4o (Versiones Específicas)
- `gpt-4o-2024-11-20` - Versión estable específica
- `gpt-4o-2024-08-06` - Versión anterior

### GPT-4.1 (Nuevos)
- `gpt-4.1` - Modelo más nuevo
- `gpt-4.1-mini` - Versión más pequeña y rápida

### GPT-5 (Si está disponible)
- `gpt-5` - Modelo más avanzado
- `gpt-5-mini` - Versión ligera

## 🔧 Cambiar Modelo

```powershell
# Usar GPT-4o (recomendado)
.\cambiar_modelo.ps1 gpt-4o

# Usar GPT-3.5-turbo (económico)
.\cambiar_modelo.ps1 gpt-3.5-turbo

# Usar versión específica
.\cambiar_modelo.ps1 gpt-4o-2024-11-20
```

## ⚠️ Después de Cambiar

**SIEMPRE reinicia el servidor:**
```powershell
# Detén con Ctrl+C
# Reinicia:
python start_server.py
```

## 💡 Recomendación

Para desarrollo de código, usa **`gpt-4o`**:
- Mejor calidad
- Más rápido que GPT-4
- Excelente para código complejo

Si quieres ahorrar dinero, usa **`gpt-3.5-turbo`** para tareas simples.
