"""
Servidor Bridge que actúa como intermediario entre Termux y Cursor.
Maneja consultas, gestión de archivos y sincronización.
"""
import os
from pathlib import Path
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from .session_manager import SessionManager


app = FastAPI(title="Cursor-Termux Bridge Server")

# CORS para permitir conexiones desde Termux
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar origen específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar gestor de sesiones
session_manager = SessionManager()

# Configuración
WORKSPACE_PATH = os.getenv("CURSOR_WORKSPACE_PATH", ".")
API_TOKEN = os.getenv("API_TOKEN", "change-me-in-production")


# Modelos Pydantic
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    project_path: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    session_id: str


class FileContent(BaseModel):
    path: str
    content: Optional[str] = None


class FileListResponse(BaseModel):
    files: List[str]


class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    last_activity: str
    metadata: Dict


class Message(BaseModel):
    role: str
    content: str
    timestamp: str


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[Message]


# Autenticación
def verify_token(authorization: Optional[str] = Header(None)):
    """Verifica el token de autenticación."""
    if not API_TOKEN or API_TOKEN == "change-me-in-production":
        return True  # Permitir sin token en desarrollo
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return True


# Endpoints de sesiones
@app.post("/sessions", response_model=SessionInfo)
def create_session(project_path: Optional[str] = None, _: bool = Depends(verify_token)):
    """Crea una nueva sesión."""
    session_id = session_manager.create_session(project_path)
    session = session_manager.get_session(session_id)
    return SessionInfo(**session)


@app.get("/sessions", response_model=List[SessionInfo])
def list_sessions(limit: int = 50, _: bool = Depends(verify_token)):
    """Lista todas las sesiones."""
    sessions = session_manager.list_sessions(limit)
    return [SessionInfo(**s) for s in sessions]


@app.get("/sessions/{session_id}", response_model=SessionHistoryResponse)
def get_session_history(session_id: str, limit: Optional[int] = None, _: bool = Depends(verify_token)):
    """Obtiene el historial de una sesión."""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = session_manager.get_messages(session_id, limit)
    return SessionHistoryResponse(
        session_id=session_id,
        messages=[Message(**msg) for msg in messages]
    )


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str, _: bool = Depends(verify_token)):
    """Elimina una sesión."""
    session_manager.delete_session(session_id)
    return {"message": "Session deleted"}


# Endpoint de consultas
@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest, _: bool = Depends(verify_token)):
    """
    Procesa una consulta y retorna respuesta.
    En una implementación real, esto se conectaría con Cursor/IA.
    Por ahora, simula una respuesta básica.
    """
    # Obtener o crear sesión
    if not request.session_id:
        session_id = session_manager.create_session(request.project_path)
    else:
        session_id = request.session_id
        # Verificar que la sesión existe
        if not session_manager.get_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
    
    # Añadir mensaje del usuario
    session_manager.add_message(session_id, "user", request.query)
    
    # Obtener historial para contexto
    history = session_manager.get_messages(session_id)
    
    # TODO: Aquí se integraría con Cursor/IA real
    # Por ahora, respuesta simulada
    response_text = f"Recibí tu consulta: '{request.query}'\n\n"
    response_text += f"Contexto de sesión: {len(history)} mensajes anteriores.\n"
    response_text += "Esta es una respuesta simulada. En producción, aquí se conectaría con Cursor/IA."
    
    # Añadir respuesta del asistente
    session_manager.add_message(session_id, "assistant", response_text)
    
    # Actualizar metadatos si hay project_path
    if request.project_path:
        session_manager.update_metadata(session_id, project_path=request.project_path)
    
    return QueryResponse(response=response_text, session_id=session_id)


# Endpoints de archivos
@app.get("/files", response_model=FileListResponse)
def list_files(path: Optional[str] = None, _: bool = Depends(verify_token)):
    """Lista archivos del proyecto."""
    base_path = Path(WORKSPACE_PATH)
    if path:
        target_path = base_path / path
        if not str(target_path).startswith(str(base_path.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        target_path = base_path
    
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    
    files = []
    if target_path.is_file():
        files = [str(target_path.relative_to(base_path))]
    else:
        for item in target_path.rglob("*"):
            if item.is_file():
                files.append(str(item.relative_to(base_path)))
    
    return FileListResponse(files=sorted(files))


@app.get("/files/{file_path:path}", response_model=FileContent)
def get_file(file_path: str, _: bool = Depends(verify_token)):
    """Obtiene el contenido de un archivo."""
    full_path = Path(WORKSPACE_PATH) / file_path
    
    # Validar que el archivo está dentro del workspace
    if not str(full_path.resolve()).startswith(str(Path(WORKSPACE_PATH).resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="Path is not a file")
    
    try:
        content = full_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File is not a text file")
    
    return FileContent(path=file_path, content=content)


@app.post("/files/{file_path:path}", response_model=FileContent)
def save_file(file_path: str, content: FileContent, _: bool = Depends(verify_token)):
    """Guarda o actualiza un archivo."""
    full_path = Path(WORKSPACE_PATH) / file_path
    
    # Validar que el archivo está dentro del workspace
    if not str(full_path.resolve()).startswith(str(Path(WORKSPACE_PATH).resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Crear directorios padre si no existen
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo
    full_path.write_text(content.content or "", encoding="utf-8")
    
    return FileContent(path=file_path, content=content.content)


@app.delete("/files/{file_path:path}")
def delete_file(file_path: str, _: bool = Depends(verify_token)):
    """Elimina un archivo."""
    full_path = Path(WORKSPACE_PATH) / file_path
    
    # Validar que el archivo está dentro del workspace
    if not str(full_path.resolve()).startswith(str(Path(WORKSPACE_PATH).resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    full_path.unlink()
    return {"message": "File deleted"}


# Endpoint de sincronización
@app.post("/sync")
def sync_files(_: bool = Depends(verify_token)):
    """
    Sincroniza archivos mediante Git.
    En una implementación real, ejecutaría git pull/push.
    """
    # TODO: Implementar sincronización Git real
    return {"message": "Sync endpoint - to be implemented with Git"}


@app.get("/health")
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando."""
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
