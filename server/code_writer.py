"""
Módulo para escribir código directamente en archivos usando IA.
"""
import re
from pathlib import Path
from typing import Optional, Dict
from .ai_integration import AIIntegration


class CodeWriter:
    """Escribe código en archivos usando IA."""
    
    def __init__(self):
        self.ai = AIIntegration()
    
    def write_code_to_file(self, query: str, file_path: str, history: list, workspace_path: str = ".") -> Dict:
        """
        Genera código usando IA y lo escribe en un archivo.
        
        Returns:
            {
                "success": bool,
                "file_path": str,
                "code": str,
                "explanation": str,
                "error": str (si hay error)
            }
        """
        try:
            # Generar código con IA
            code_data = self.ai.generate_code(query, history, file_path)
            
            code = code_data.get("code", "")
            explanation = code_data.get("explanation", "")
            
            if not code:
                return {
                    "success": False,
                    "error": "No se pudo generar código",
                    "file_path": file_path
                }
            
            # Limpiar código (remover markdown si está presente)
            code = self._clean_code(code)
            
            # Escribir archivo
            full_path = Path(workspace_path) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            full_path.write_text(code, encoding="utf-8")
            
            return {
                "success": True,
                "file_path": file_path,
                "code": code,
                "explanation": explanation
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    def _clean_code(self, code: str) -> str:
        """Limpia el código removiendo bloques markdown si están presentes."""
        # Remover bloques de código markdown
        code = re.sub(r'```[a-z]*\n', '', code)
        code = re.sub(r'```\n?$', '', code)
        code = code.strip()
        return code
