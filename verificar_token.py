#!/usr/bin/env python3
"""
Script para verificar si un token funciona con el servidor
"""
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def verify_token(token, server_url=None):
    """Verifica si un token funciona con el servidor."""
    if not server_url:
        server_url = os.getenv("CURSOR_SERVER_URL", "http://localhost:8000")
    
    # Probar endpoint que requiere autenticación
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Probar con /sessions (requiere autenticación)
        response = requests.get(f"{server_url}/sessions", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print(f"[OK] Token valido! El servidor acepto el token.")
            return True
        elif response.status_code == 401:
            print(f"[ERROR] Token invalido. El servidor rechazo el token (401 Unauthorized).")
            return False
        else:
            print(f"[ADVERTENCIA] Respuesta inesperada: {response.status_code}")
            print(f"  {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] No se pudo conectar al servidor en {server_url}")
        print(f"  Verifica que el servidor este corriendo")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Leer token del .env si no se proporciona
        token = os.getenv("API_TOKEN")
        if not token:
            print("Uso: python verificar_token.py <token>")
            print("O configura API_TOKEN en .env")
            sys.exit(1)
    else:
        token = sys.argv[1]
    
    server_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Verificando token: {token[:20]}...")
    print(f"Servidor: {server_url or os.getenv('CURSOR_SERVER_URL', 'http://localhost:8000')}")
    print()
    
    verify_token(token, server_url)
