#!/usr/bin/env python3
"""
Cliente CLI para Termux que interactúa con el servidor Bridge.
Permite hacer consultas, editar archivos, sincronizar y gestionar sesiones.
"""
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Optional
import click
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
CONFIG_DIR = Path.home() / ".cursor_termux"
CONFIG_DIR.mkdir(exist_ok=True)
SESSION_FILE = CONFIG_DIR / "session_id"
CONFIG_FILE = CONFIG_DIR / "config.json"

SERVER_URL = os.getenv("CURSOR_SERVER_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "")


class CursorClient:
    def __init__(self, server_url: str = SERVER_URL, api_token: str = API_TOKEN):
        """Inicializa el cliente."""
        self.server_url = server_url.rstrip("/")
        self.api_token = api_token
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Hace una petición HTTP al servidor."""
        url = f"{self.server_url}{endpoint}"
        kwargs.setdefault("headers", {}).update(self.headers)
        
        try:
            response = requests.request(method, url, **kwargs, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError:
            click.echo(f"Error: No se pudo conectar al servidor en {self.server_url}", err=True)
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            click.echo(f"Error HTTP: {e}", err=True)
            if e.response.status_code == 401:
                click.echo("Verifica tu API_TOKEN", err=True)
            sys.exit(1)
    
    def get_active_session(self) -> Optional[str]:
        """Obtiene la sesión activa."""
        if SESSION_FILE.exists():
            return SESSION_FILE.read_text().strip()
        return None
    
    def set_active_session(self, session_id: str):
        """Establece la sesión activa."""
        SESSION_FILE.write_text(session_id)
    
    def query(self, query_text: str, session_id: Optional[str] = None, new_session: bool = False) -> dict:
        """Envía una consulta al servidor."""
        if new_session:
            session_id = None
        elif not session_id:
            session_id = self.get_active_session()
        
        data = {
            "query": query_text,
            "session_id": session_id
        }
        
        response = self._request("POST", "/query", json=data)
        result = response.json()
        
        # Guardar session_id si es nueva
        if result.get("session_id"):
            self.set_active_session(result["session_id"])
        
        return result
    
    def list_sessions(self) -> list:
        """Lista todas las sesiones."""
        response = self._request("GET", "/sessions")
        return response.json()
    
    def get_session_history(self, session_id: Optional[str] = None) -> dict:
        """Obtiene el historial de una sesión."""
        if not session_id:
            session_id = self.get_active_session()
            if not session_id:
                click.echo("No hay sesión activa", err=True)
                sys.exit(1)
        
        response = self._request("GET", f"/sessions/{session_id}")
        return response.json()
    
    def delete_session(self, session_id: str):
        """Elimina una sesión."""
        self._request("DELETE", f"/sessions/{session_id}")
    
    def list_files(self, path: Optional[str] = None) -> list:
        """Lista archivos del proyecto."""
        params = {}
        if path:
            params["path"] = path
        
        response = self._request("GET", "/files", params=params)
        return response.json()["files"]
    
    def get_file(self, file_path: str) -> str:
        """Obtiene el contenido de un archivo."""
        response = self._request("GET", f"/files/{file_path}")
        return response.json()["content"]
    
    def save_file(self, file_path: str, content: str):
        """Guarda un archivo."""
        data = {"content": content}
        self._request("POST", f"/files/{file_path}", json=data)
    
    def sync(self):
        """Sincroniza archivos."""
        response = self._request("POST", "/sync")
        return response.json()


# CLI Commands
@click.group()
@click.option("--server-url", envvar="CURSOR_SERVER_URL", default=SERVER_URL, help="URL del servidor")
@click.option("--api-token", envvar="API_TOKEN", default=API_TOKEN, help="Token de autenticación")
@click.pass_context
def cli(ctx, server_url, api_token):
    """Cliente CLI para Cursor-Termux Bridge."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = CursorClient(server_url, api_token)


@cli.command()
@click.argument("query", required=True)
@click.option("--new-session", "-n", is_flag=True, help="Crear nueva sesión")
@click.pass_context
def query(ctx, query, new_session):
    """Hace una consulta al asistente."""
    client = ctx.obj["client"]
    
    result = client.query(query, new_session=new_session)
    
    click.echo("\n" + "="*60)
    click.echo(result["response"])
    click.echo("="*60)
    click.echo(f"\nSesión: {result['session_id']}")


@cli.command()
@click.pass_context
def sessions(ctx):
    """Lista todas las sesiones."""
    client = ctx.obj["client"]
    
    sessions_list = client.list_sessions()
    active_session = client.get_active_session()
    
    if not sessions_list:
        click.echo("No hay sesiones")
        return
    
    click.echo("\nSesiones:")
    click.echo("-" * 80)
    for session in sessions_list:
        marker = " * " if session["session_id"] == active_session else "   "
        click.echo(f"{marker}{session['session_id']}")
        click.echo(f"    Creada: {session['created_at']}")
        click.echo(f"    Última actividad: {session['last_activity']}")
        click.echo()


@cli.command()
@click.argument("session_id")
@click.pass_context
def session(ctx, session_id):
    """Cambia a otra sesión."""
    client = ctx.obj["client"]
    client.set_active_session(session_id)
    click.echo(f"Sesión activa: {session_id}")


@cli.command()
@click.pass_context
def history(ctx):
    """Muestra el historial de la sesión actual."""
    client = ctx.obj["client"]
    
    active_session = client.get_active_session()
    if not active_session:
        click.echo("No hay sesión activa", err=True)
        sys.exit(1)
    
    history_data = client.get_session_history(active_session)
    
    click.echo(f"\nHistorial de sesión: {active_session}")
    click.echo("=" * 80)
    
    for msg in history_data["messages"]:
        role_color = "green" if msg["role"] == "user" else "blue"
        click.echo(f"\n[{msg['role'].upper()}] ({msg['timestamp']})")
        click.echo(click.style(msg["content"], fg=role_color))
        click.echo("-" * 80)


@cli.command()
@click.argument("file_paths", nargs=-1, required=True)
@click.option("--no-sync", is_flag=True, help="No sincronizar automáticamente después de editar")
@click.pass_context
def edit(ctx, file_paths, no_sync):
    """Abre nano para editar uno o más archivos."""
    client = ctx.obj["client"]
    
    # Importar wrapper de nano
    from .nano_wrapper import edit_with_nano, edit_multiple_files
    
    if len(file_paths) == 1:
        edit_with_nano(client, file_paths[0], auto_sync=not no_sync)
    else:
        edit_multiple_files(client, list(file_paths), auto_sync=not no_sync)


@cli.command()
@click.argument("file_path")
@click.pass_context
def open(ctx, file_path):
    """Muestra el contenido de un archivo sin editar."""
    client = ctx.obj["client"]
    
    try:
        content = client.get_file(file_path)
        click.echo(content)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """Lista archivos del proyecto."""
    client = ctx.obj["client"]
    
    try:
        files = client.list_files()
        for file in files:
            click.echo(file)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def sync(ctx):
    """Sincroniza archivos con el servidor."""
    client = ctx.obj["client"]
    
    try:
        result = client.sync()
        click.echo(result.get("message", "Sincronización completada"))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
