"""
Gestor de sesiones para mantener contexto de conversaciones.
Almacena historial de mensajes en SQLite.
"""
import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class SessionManager:
    def __init__(self, db_path: str = "sessions.db"):
        """Inicializa el gestor de sesiones con base de datos SQLite."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Crea las tablas necesarias si no existen."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de sesiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                last_activity TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        # Tabla de mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_session(self, project_path: Optional[str] = None) -> str:
        """Crea una nueva sesión y retorna su ID."""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        metadata = {
            "project_path": project_path,
            "active_files": []
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (session_id, created_at, last_activity, metadata)
            VALUES (?, ?, ?, ?)
        """, (session_id, now, now, json.dumps(metadata)))
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str):
        """Añade un mensaje a una sesión."""
        if role not in ["user", "assistant", "system"]:
            raise ValueError("Role must be 'user', 'assistant', or 'system'")
        
        now = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (session_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, role, content, now))
        
        # Actualizar last_activity
        cursor.execute("""
            UPDATE sessions SET last_activity = ? WHERE session_id = ?
        """, (now, session_id))
        
        conn.commit()
        conn.close()
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Obtiene los mensajes de una sesión."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT role, content, timestamp
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (session_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "role": row["role"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            }
            for row in rows
        ]
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Obtiene información de una sesión."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT session_id, created_at, last_activity, metadata
            FROM sessions
            WHERE session_id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "last_activity": row["last_activity"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
        }
    
    def list_sessions(self, limit: int = 50) -> List[Dict]:
        """Lista todas las sesiones ordenadas por última actividad."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT session_id, created_at, last_activity, metadata
            FROM sessions
            ORDER BY last_activity DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "session_id": row["session_id"],
                "created_at": row["created_at"],
                "last_activity": row["last_activity"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
            }
            for row in rows
        ]
    
    def delete_session(self, session_id: str):
        """Elimina una sesión y todos sus mensajes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
    
    def update_metadata(self, session_id: str, **kwargs):
        """Actualiza los metadatos de una sesión."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        metadata = session["metadata"]
        metadata.update(kwargs)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE sessions SET metadata = ? WHERE session_id = ?
        """, (json.dumps(metadata), session_id))
        
        conn.commit()
        conn.close()
