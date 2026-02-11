#!/usr/bin/env python3
"""
Script para generar un token seguro para API_TOKEN
"""
import secrets
import string

def generate_token(length=32):
    """Genera un token seguro aleatorio."""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token

if __name__ == "__main__":
    token = generate_token(32)
    print(f"\nToken generado: {token}")
    print(f"\nAñade esta línea a tu archivo .env:")
    print(f"API_TOKEN={token}\n")
