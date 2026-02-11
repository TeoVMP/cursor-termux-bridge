"""
Wrapper para nano que detecta cuando se cierra el editor
y sincroniza cambios automáticamente con el servidor.
"""
import os
import subprocess
import hashlib
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime
import click


def calculate_file_hash(file_path: Path) -> str:
    """Calcula el hash MD5 de un archivo."""
    if not file_path.exists():
        return ""
    
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_backup(file_path: Path, backup_dir: Path) -> Path:
    """Crea un backup del archivo antes de editar."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.name}.{timestamp}"
    backup_path = backup_dir / backup_name
    
    if file_path.exists():
        shutil.copy2(file_path, backup_path)
    
    return backup_path


def edit_with_nano(client, file_path: str, auto_sync: bool = True):
    """
    Abre nano para editar un archivo y sincroniza cambios automáticamente.
    
    Args:
        client: Instancia de CursorClient
        file_path: Ruta del archivo a editar
        auto_sync: Si True, sincroniza automáticamente después de editar
    """
    # Crear directorio temporal local para trabajar
    local_dir = Path.home() / ".cursor_termux" / "local_files"
    local_dir.mkdir(parents=True, exist_ok=True)
    
    local_file = local_dir / file_path.replace("/", "_").replace("\\", "_")
    backup_dir = Path.home() / ".cursor_termux" / ".backup"
    
    # Descargar archivo del servidor si existe
    try:
        content = client.get_file(file_path)
        local_file.write_text(content, encoding="utf-8")
        click.echo(f"Archivo descargado: {file_path}")
    except Exception:
        # Archivo no existe, crear uno nuevo
        local_file.touch()
        click.echo(f"Creando nuevo archivo: {file_path}")
    
    # Crear backup
    backup_path = create_backup(local_file, backup_dir)
    
    # Calcular hash antes de editar
    hash_before = calculate_file_hash(local_file)
    
    # Abrir nano
    click.echo(f"\nEditando con nano... (Ctrl+X para salir, Ctrl+O para guardar)")
    click.echo(f"Archivo local: {local_file}")
    
    # Verificar que nano está instalado
    nano_path = shutil.which("nano")
    if not nano_path:
        click.echo("Error: nano no está instalado", err=True)
        click.echo("Instala nano con: pkg install nano", err=True)
        return
    
    # Ejecutar nano
    try:
        result = subprocess.run(
            [nano_path, str(local_file)],
            check=False
        )
        exit_code = result.returncode
    except KeyboardInterrupt:
        click.echo("\nEdición cancelada por el usuario")
        return
    except Exception as e:
        click.echo(f"Error al ejecutar nano: {e}", err=True)
        return
    
    # Calcular hash después de editar
    hash_after = calculate_file_hash(local_file)
    
    # Verificar si hubo cambios
    if hash_before == hash_after:
        click.echo("\nNo se detectaron cambios")
        return
    
    # Leer contenido editado
    try:
        edited_content = local_file.read_text(encoding="utf-8")
    except Exception as e:
        click.echo(f"Error al leer archivo editado: {e}", err=True)
        return
    
    # Subir cambios al servidor
    if auto_sync:
        click.echo("\nSincronizando cambios con el servidor...")
        try:
            client.save_file(file_path, edited_content)
            click.echo(click.style("✓ Cambios sincronizados exitosamente", fg="green"))
        except Exception as e:
            click.echo(click.style(f"✗ Error al sincronizar: {e}", fg="red"), err=True)
            click.echo(f"El archivo local está guardado en: {local_file}", err=True)
            click.echo(f"Backup disponible en: {backup_path}", err=True)
    else:
        click.echo(f"\nArchivo editado guardado localmente en: {local_file}")
        click.echo("Usa 'cursor sync' para sincronizar manualmente")


def edit_multiple_files(client, file_paths: list, auto_sync: bool = True):
    """
    Edita múltiples archivos secuencialmente.
    
    Args:
        client: Instancia de CursorClient
        file_paths: Lista de rutas de archivos a editar
        auto_sync: Si True, sincroniza automáticamente después de cada edición
    """
    for i, file_path in enumerate(file_paths, 1):
        click.echo(f"\n[{i}/{len(file_paths)}] Editando: {file_path}")
        edit_with_nano(client, file_path, auto_sync=auto_sync)
        
        if i < len(file_paths):
            if not click.confirm("\n¿Continuar con el siguiente archivo?"):
                break
