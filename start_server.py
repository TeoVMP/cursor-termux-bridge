#!/usr/bin/env python3
"""
Script de inicio rápido para el servidor bridge.
"""
import os
import sys
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    import uvicorn
    from server.bridge_server import app
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Iniciando servidor en http://{host}:{port}")
    print("Presiona Ctrl+C para detener")
    
    uvicorn.run(app, host=host, port=port)
