# 🔧 Solución: Timeout en Termux

## Cambios Aplicados

1. ✅ **Timeout aumentado a 5 minutos** (300 segundos) en cliente Termux
2. ✅ **Prompts simplificados** para que Ollama responda más rápido
3. ✅ **Integración inteligente solo para archivos existentes** (archivos nuevos usan overwrite automático)

## Actualizar Código en Termux

```bash
git pull
```

## Probar de Nuevo

```bash
# Probar con archivo nuevo (más rápido, sin integración)
cursor query "Crea una función que sume dos números" --write suma.py
```

## Si Sigue Siendo Muy Lento

### Opción 1: Probar Sin Integración Inteligente

Para archivos nuevos, ya no usa integración (más rápido). Para archivos existentes, puedes forzar overwrite:

```bash
cursor query "Reemplaza todo con función suma" --write suma.py
```

### Opción 2: Usar Modelo Más Rápido

```powershell
# En ordenador
.\cambiar_modelo.ps1 mistral
# Reiniciar servidor
```

### Opción 3: Ver Logs del Servidor

En la terminal donde corre el servidor, deberías ver:
- Cuándo recibe la petición
- Cuándo llama a Ollama  
- Cuándo termina

Si no ves actividad después de recibir la petición, Ollama puede estar bloqueado.

### Opción 4: Probar Consulta Simple Primero

```bash
# Probar sin escribir archivo (más rápido)
cursor query "Hola, ¿funcionas?"

# Si esto funciona rápido, el problema es la generación de código
```

## Verificar Ollama en Servidor

```powershell
# En ordenador, probar Ollama directamente
ollama run codellama "Escribe función Python suma"

# Si esto tarda más de 2 minutos, Ollama es el problema
```

## Notas

- ✅ Timeout aumentado a 5 minutos
- ✅ Prompts simplificados (más rápidos)
- ✅ Archivos nuevos no usan integración (más rápido)
- ⚠️ Ollama puede ser lento, especialmente primera consulta
- ⚠️ Es normal que tarde 1-3 minutos con Ollama
