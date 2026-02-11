# 🧠 Integración Inteligente de Código

## ¿Cómo Funciona?

El sistema ahora tiene **dos modos** de escritura:

### 1. Modo Integración (Por Defecto) 🧠

Cuando escribes código en un archivo que **ya existe**, el sistema:

1. ✅ **Lee el código existente**
2. ✅ **Analiza la estructura y funcionalidad**
3. ✅ **Integra el nuevo código de forma inteligente**
4. ✅ **Mantiene todo el código existente que no se modifica**
5. ✅ **Respeta el estilo y estructura original**

**Ejemplo:**
```bash
# Archivo existente: suma.py
def suma(a, b):
    return a + b

# Consulta:
cursor query "Añade una función que reste" --write suma.py

# Resultado (integrado):
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b
```

### 2. Modo Sobrescritura (Explícito) 📝

Si quieres **sobrescribir completamente** el archivo:

```bash
# Usa palabras clave en la consulta:
cursor query "Reemplaza todo el código con una nueva implementación" --write archivo.py
# o
cursor query "Sobrescribe el archivo con..." --write archivo.py
```

Palabras clave que activan modo overwrite:
- "sobrescribir"
- "reemplazar" 
- "overwrite"
- "replace"

## Ejemplos de Integración Inteligente

### Añadir Funcionalidad

```bash
# Archivo existente tiene función suma()
cursor query "Añade función multiplicar" --write calculadora.py

# La IA añade la nueva función SIN eliminar la existente
```

### Modificar Funcionalidad Existente

```bash
# Archivo tiene función suma() básica
cursor query "Mejora la función suma para manejar listas" --write calculadora.py

# La IA modifica SOLO esa función, mantiene el resto
```

### Añadir Validación

```bash
# Archivo tiene funciones sin validación
cursor query "Añade validación de tipos a todas las funciones" --write calculadora.py

# La IA añade validaciones manteniendo la lógica existente
```

### Crear Archivo Nuevo

```bash
# Archivo no existe
cursor query "Crea una clase Usuario" --write usuario.py

# Crea el archivo completo (modo overwrite automático)
```

## Ventajas de la Integración Inteligente

### ✅ Preserva Código Existente
- No pierdes código que no quieres modificar
- Mantiene imports y configuración

### ✅ Respeta Estilo
- Mantiene el estilo de código existente
- Respeta indentación y formato

### ✅ Integración Contextual
- Entiende la estructura del código
- Añade código en lugares apropiados

### ✅ Funcionalidad Completa
- El código resultante es válido y funcional
- No rompe dependencias existentes

## Cómo Funciona Internamente

1. **Lee el archivo existente** (si existe)
2. **Envía a la IA:**
   - Código existente completo
   - Consulta del usuario
   - Instrucciones de integración
3. **La IA analiza y genera:**
   - Código completo integrado
   - Manteniendo funcionalidad existente
   - Añadiendo/modificando según consulta
4. **Escribe el resultado** integrado

## Comparación con Cursor

**Cursor Composer:**
- ✅ Integra código inteligentemente
- ✅ Mantiene código existente
- ✅ Respeta estructura

**Este Sistema:**
- ✅ Hace lo mismo que Cursor
- ✅ Funciona desde terminal
- ✅ Con modelos gratuitos (Ollama)

## Tips para Mejores Resultados

### Sé Específico
```bash
# ✅ Bueno
cursor query "Añade función resta después de la función suma" --write calculadora.py

# ❌ Menos claro
cursor query "añade resta" --write calculadora.py
```

### Indica Ubicación
```bash
# ✅ Específico
cursor query "Añade validación al inicio de la función" --write archivo.py

# ✅ También funciona
cursor query "Añade validación" --write archivo.py
```

### Para Sobrescribir
```bash
# ✅ Explícito
cursor query "Reemplaza todo con nueva implementación" --write archivo.py
```

## Troubleshooting

### El código no se integra bien
- Sé más específico en tu consulta
- Indica qué parte modificar
- Usa modo overwrite si necesitas empezar de cero

### Se pierde código importante
- Revisa el archivo antes de confirmar
- Usa `cursor open archivo.py` para verificar
- Puedes revertir con git si es necesario

### Quieres sobrescribir pero se integra
- Usa palabras clave: "sobrescribir", "reemplazar"
- O edita manualmente con `cursor edit`
