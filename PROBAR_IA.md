# 🧪 Probar que la IA Funciona

## Pasos para Probar

### 1. Verificar que el servidor está corriendo

En tu ordenador:
```powershell
# El servidor debe estar corriendo
# Si no, inícialo:
python start_server.py
```

### 2. Probar desde Termux

```bash
# Consulta simple
cursor query "Hola, ¿funcionas con IA real?"

# Deberías ver una respuesta real de GPT-4, no la respuesta simulada
```

### 3. Probar Generación de Código

```bash
# Generar código y escribirlo en archivo
cursor query "Crea una función Python que sume dos números" --write test_suma.py

# Ver el código generado
cursor open test_suma.py
```

### 4. Verificar que el Código se Escribió

```bash
# En el servidor (ordenador), verifica que el archivo existe
# Deberías ver test_suma.py en la carpeta del proyecto
```

## Si No Funciona

### Error: "AI_PROVIDER no configurado"
- Verifica que `.env` tenga `AI_PROVIDER=openai`
- Reinicia el servidor

### Error: "API key no configurada"
- Verifica que `.env` tenga `OPENAI_API_KEY=sk-proj-...`
- Verifica que no haya espacios extra

### Error: "No module named 'openai'"
```powershell
# Instala la librería
.\venv\Scripts\Activate.ps1
pip install openai
```

### Error: "Invalid API key"
- Verifica que la API key sea correcta
- Verifica que tengas créditos en OpenAI
- Ve a https://platform.openai.com/account/usage

### Respuesta Simulada Todavía
- Reinicia el servidor completamente
- Verifica los logs del servidor para ver errores
- Verifica que `.env` esté en la carpeta correcta

## Ver Logs del Servidor

Cuando ejecutas el servidor, deberías ver logs. Si hay errores con la IA, aparecerán ahí.

## Próximo Paso

Una vez que funcione, puedes empezar a generar código:

```bash
cursor query "Crea un script Python completo que..." --write archivo.py
```
