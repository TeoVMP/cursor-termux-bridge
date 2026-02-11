# 💻 Escribir Código en Tiempo Real con IA

## 🎯 Funcionalidad Principal

Ahora puedes pedirle a la IA que escriba código directamente en archivos desde tu teléfono usando Termux.

## 🚀 Configuración Rápida

### Paso 1: Configurar IA en el Servidor

1. **Elige un proveedor de IA** (OpenAI recomendado para empezar):
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Ollama: https://ollama.ai/ (gratis, local)

2. **Edita `.env` en tu servidor:**
   ```bash
   # Para OpenAI
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-tu-api-key-aqui
   OPENAI_MODEL=gpt-4
   ```

3. **Instala la librería necesaria:**
   ```bash
   pip install openai  # Para OpenAI
   # o
   pip install anthropic  # Para Anthropic
   ```

4. **Reinicia el servidor**

## 📱 Uso desde Termux

### Consulta Normal (Solo Respuesta)
```bash
cursor query "¿Cómo creo una función en Python?"
```

### Generar Código y Escribirlo en Archivo
```bash
cursor query "Crea una función que sume dos números" --write suma.py
```

La IA generará el código y lo escribirá automáticamente en `suma.py`.

## 🎨 Ejemplos Prácticos

### Crear Scripts Completos

```bash
# Script Python
cursor query "Crea un script que lea un archivo JSON y muestre su contenido" --write leer_json.py

# Script con clase
cursor query "Crea una clase Usuario con nombre, email y método para mostrar info" --write usuario.py

# Script con validación
cursor query "Crea una función que valide emails usando regex" --write validar_email.py
```

### Crear Archivos HTML/CSS/JS

```bash
# HTML
cursor query "Crea una página HTML con un formulario de contacto" --write contacto.html

# CSS
cursor query "Crea estilos CSS para el formulario, hazlo moderno y responsive" --write estilo.css

# JavaScript
cursor query "Añade validación JavaScript al formulario" --write validacion.js
```

### Modificar Código Existente

```bash
# Primero pregunta qué hacer
cursor query "Añade validación de email a la clase Usuario en usuario.py" --write usuario.py

# O mejora código existente
cursor query "Optimiza la función suma para manejar listas de números" --write suma.py
```

### Crear Múltiples Archivos

```bash
# Crea los archivos uno por uno
cursor query "Crea un archivo config.py con configuración de base de datos" --write config.py
cursor query "Crea un archivo database.py que use la configuración" --write database.py
cursor query "Crea un archivo main.py que importe y use database" --write main.py
```

## 🔄 Flujo de Trabajo Completo

1. **Hacer consulta y generar código:**
   ```bash
   cursor query "Crea una API REST con FastAPI que tenga endpoints para usuarios" --write api.py
   ```

2. **Ver el código generado:**
   ```bash
   cursor open api.py
   ```

3. **Editar si es necesario:**
   ```bash
   cursor edit api.py
   ```

4. **Hacer más consultas relacionadas:**
   ```bash
   cursor query "Añade autenticación JWT a la API" --write api.py
   ```

5. **Ver historial completo:**
   ```bash
   cursor history
   ```

## 💡 Tips

### Usar Contexto
El sistema mantiene contexto entre consultas, así que puedes hacer:
```bash
cursor query "Crea una función suma" --write calculadora.py
cursor query "Añade función resta" --write calculadora.py
cursor query "Añade función multiplicar" --write calculadora.py
```

### Especificar Lenguaje
```bash
cursor query "Crea una función en JavaScript que valide emails" --write validar.js
cursor query "Crea la misma función pero en Python" --write validar.py
```

### Crear Proyectos Completos
```bash
# Estructura básica
cursor query "Crea un proyecto Flask con estructura de carpetas" --write app.py
cursor query "Crea requirements.txt con Flask y otras dependencias" --write requirements.txt
cursor query "Crea README.md con instrucciones" --write README.md
```

## ⚙️ Configuración Avanzada

### Cambiar Modelo de IA

En `.env`:
```bash
# GPT-4 (mejor calidad, más caro)
OPENAI_MODEL=gpt-4

# GPT-3.5 (más barato, rápido)
OPENAI_MODEL=gpt-3.5-turbo

# Claude Opus (muy buena calidad)
ANTHROPIC_MODEL=claude-3-opus-20240229
```

### Usar Modelo Local (Gratis)

```bash
# Instala Ollama
# Descarga modelo: ollama pull codellama

# En .env:
AI_PROVIDER=ollama
OLLAMA_MODEL=codellama
```

## 🐛 Troubleshooting

### El código no se escribe
- Verifica que el servidor tenga permisos de escritura
- Revisa los logs del servidor
- Verifica que la API key sea válida

### Respuesta de error de IA
- Verifica tu balance/créditos en la plataforma
- Verifica que el modelo esté disponible
- Si usas modelo local, verifica que esté corriendo

### Código mal formateado
- Especifica mejor tu consulta
- Usa modelos más avanzados (GPT-4, Claude Opus)
- Puedes editar manualmente después con `cursor edit`

## 🎉 ¡Listo!

Ahora puedes escribir código en tiempo real desde tu teléfono usando IA. Solo haz consultas y especifica `--write archivo.py` para que la IA escriba el código directamente.
