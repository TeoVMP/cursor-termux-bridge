# 🔍 Diagnóstico: Timeout en Termux

## Problema

- ✅ Funciona en ordenador
- ❌ Timeout en Termux después de 120 segundos
- El servidor está tardando más de 2 minutos

## Posibles Causas

### 1. Ollama Muy Lento
Ollama puede tardar mucho, especialmente:
- Primera consulta (carga modelo)
- Integración inteligente (analiza código existente)
- Código complejo

### 2. Red Lenta
La conexión entre Termux y el servidor puede ser lenta.

### 3. Procesamiento Pesado
La integración inteligente requiere:
- Leer archivo existente
- Enviar a IA (código completo + consulta)
- Generar código integrado
- Escribir archivo

## Soluciones

### Solución 1: Aumentar Timeout Más

**En Termux, edita `termux/cursor_client.py`:**
```python
# Línea ~45, cambiar a:
timeout_value = kwargs.pop('timeout', 300)  # 5 minutos
```

### Solución 2: Usar Modelo Más Rápido

```powershell
# En ordenador
.\cambiar_modelo.ps1 mistral
# Reiniciar servidor
```

### Solución 3: Desactivar Integración Inteligente Temporalmente

Para pruebas rápidas, puedes modificar el código para usar modo overwrite siempre.

### Solución 4: Verificar Logs del Servidor

En la terminal donde corre el servidor, deberías ver:
- Cuándo recibe la petición
- Cuándo llama a Ollama
- Cuándo termina

Si no ves logs después de recibir la petición, Ollama puede estar bloqueado.

## Verificación Rápida

### 1. Probar Ollama Directamente en Servidor

```powershell
# En ordenador, probar Ollama directamente
ollama run codellama "Escribe una función Python que sume dos números"
```

Si esto tarda más de 2 minutos, Ollama es el problema.

### 2. Probar Consulta Simple Sin Archivo

```bash
# En Termux, probar sin --write
cursor query "Hola, ¿funcionas?"
```

Si esto funciona rápido, el problema es la generación de código.

### 3. Probar con Archivo Nuevo (Sin Integración)

```bash
# Crear archivo nuevo (no existe, no hay integración)
cursor query "Crea función suma" --write nuevo.py
```

Si esto funciona, el problema es la integración inteligente.

## Solución Temporal: Modo Simple

Puedes modificar temporalmente para usar modo overwrite siempre:

**En `server/bridge_server.py`, línea ~162:**
```python
# Cambiar de:
mode = "overwrite" if any(...) else "integrate"

# A:
mode = "overwrite"  # Temporalmente, para pruebas
```

Esto evitará la integración inteligente y será más rápido.

## Próximos Pasos

1. Verificar logs del servidor
2. Probar Ollama directamente
3. Probar consulta simple sin archivo
4. Si funciona, aumentar timeout o usar modelo más rápido
