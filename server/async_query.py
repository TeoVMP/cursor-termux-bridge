"""
Módulo para manejar consultas asíncronas y evitar timeouts.
"""
import asyncio
from fastapi import BackgroundTasks
from typing import Optional, Dict
import uuid
import time
from .session_manager import SessionManager
from .ai_integration import AIIntegration
from .code_writer import CodeWriter


class AsyncQueryHandler:
    """Maneja consultas asíncronas para evitar timeouts."""
    
    def __init__(self):
        self.ai = AIIntegration()
        self.code_writer = CodeWriter()
        self.pending_queries = {}  # {query_id: {status, result, error}}
    
    def process_query_async(self, query: str, session_id: str, history: list, 
                           write_to_file: Optional[str] = None, workspace_path: str = ".") -> Dict:
        """
        Procesa una consulta de forma asíncrona y retorna inmediatamente con un query_id.
        El resultado se puede obtener después con get_query_result.
        """
        query_id = str(uuid.uuid4())
        
        # Inicializar estado
        self.pending_queries[query_id] = {
            "status": "processing",
            "result": None,
            "error": None,
            "created_at": time.time()
        }
        
        # Procesar en background (simulado, en producción usar BackgroundTasks)
        try:
            # Llamar a la IA
            response_text = self.ai.chat(history, query)
            
            # Si se solicita escribir código
            if write_to_file:
                result = self.code_writer.write_code_to_file(
                    query,
                    write_to_file,
                    history,
                    workspace_path,
                    mode="integrate"
                )
                
                if result["success"]:
                    response_text += f"\n\n✅ Código integrado en: {result['file_path']}\n"
                    response_text += f"📝 {result.get('explanation', '')}"
                else:
                    response_text += f"\n\n❌ Error: {result.get('error', 'Unknown error')}"
            
            # Guardar resultado
            self.pending_queries[query_id] = {
                "status": "completed",
                "result": response_text,
                "error": None,
                "completed_at": time.time()
            }
            
        except Exception as e:
            self.pending_queries[query_id] = {
                "status": "error",
                "result": None,
                "error": str(e),
                "completed_at": time.time()
            }
        
        return {
            "query_id": query_id,
            "status": "processing",
            "message": "Consulta en proceso. Usa /query/{query_id} para obtener el resultado."
        }
    
    def get_query_result(self, query_id: str) -> Optional[Dict]:
        """Obtiene el resultado de una consulta asíncrona."""
        if query_id not in self.pending_queries:
            return None
        
        query_data = self.pending_queries[query_id]
        
        if query_data["status"] == "completed":
            return {
                "query_id": query_id,
                "status": "completed",
                "result": query_data["result"]
            }
        elif query_data["status"] == "error":
            return {
                "query_id": query_id,
                "status": "error",
                "error": query_data["error"]
            }
        else:
            return {
                "query_id": query_id,
                "status": "processing",
                "message": "Consulta aún en proceso..."
            }
