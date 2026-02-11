"""
Módulo para escribir código directamente en archivos usando IA.
"""
import re
import json
from pathlib import Path
from typing import Optional, Dict
from .ai_integration import AIIntegration


class CodeWriter:
    """Escribe código en archivos usando IA."""
    
    def __init__(self):
        self.ai = AIIntegration()
    
    def write_code_to_file(self, query: str, file_path: str, history: list, workspace_path: str = ".", mode: str = "integrate") -> Dict:
        """
        Genera código usando IA y lo escribe/integra en un archivo.
        
        Args:
            query: Consulta del usuario
            file_path: Ruta del archivo
            history: Historial de conversación
            workspace_path: Ruta del workspace
            mode: "integrate" (inteligente) o "overwrite" (sobrescribir)
        
        Returns:
            {
                "success": bool,
                "file_path": str,
                "code": str,
                "explanation": str,
                "mode": str,
                "error": str (si hay error)
            }
        """
        try:
            full_path = Path(workspace_path) / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Leer código existente si el archivo existe
            existing_code = ""
            file_exists = full_path.exists()
            
            if file_exists:
                try:
                    existing_code = full_path.read_text(encoding="utf-8")
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Error al leer archivo existente: {str(e)}",
                        "file_path": file_path
                    }
            
            # Si el archivo existe y modo es "integrate", usar integración inteligente
            if file_exists and mode == "integrate" and existing_code.strip():
                integrated_code = self._integrate_code_intelligently(query, existing_code, history, file_path)
                
                if integrated_code:
                    full_path.write_text(integrated_code, encoding="utf-8")
                    return {
                        "success": True,
                        "file_path": file_path,
                        "code": integrated_code,
                        "explanation": "Código integrado inteligentemente con el existente",
                        "mode": "integrate"
                    }
                else:
                    # Si falla la integración, intentar generación normal
                    mode = "overwrite"
            
            # Generar código nuevo (modo overwrite o archivo nuevo)
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
            full_path.write_text(code, encoding="utf-8")
            
            return {
                "success": True,
                "file_path": file_path,
                "code": code,
                "explanation": explanation,
                "mode": "overwrite" if not file_exists else "overwrite"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    def _integrate_code_intelligently(self, query: str, existing_code: str, history: list, file_path: str) -> Optional[str]:
        """
        Integra código nuevo con código existente de forma inteligente usando IA.
        """
        try:
            # Preparar prompt para integración inteligente
            integration_prompt = f"""Eres un asistente experto en programación. Necesitas integrar código nuevo con código existente.

ARCHIVO EXISTENTE ({file_path}):
```
{existing_code}
```

CONSULTA DEL USUARIO:
{query}

INSTRUCCIONES:
1. Analiza el código existente cuidadosamente
2. Integra el nuevo código/cambios solicitados de forma inteligente
3. Mantén toda la funcionalidad existente que no se modifique
4. Asegúrate de que el código resultante sea válido y funcional
5. Si el usuario pide añadir algo, añádelo sin eliminar lo existente
6. Si el usuario pide modificar algo, modifica solo esa parte
7. Si el usuario pide eliminar algo, elimínalo pero mantén el resto
8. Respeta la estructura y estilo del código existente

Responde SOLO con el código completo integrado, sin explicaciones adicionales ni markdown."""

            # Preparar mensajes con contexto
            messages = []
            messages.append({
                "role": "system",
                "content": "Eres un asistente de programación experto. Integras código nuevo con código existente de forma inteligente y optimizada."
            })
            
            # Añadir historial relevante
            for msg in history[-5:]:  # Últimos 5 mensajes para contexto
                if msg["role"] in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Añadir prompt de integración
            messages.append({
                "role": "user",
                "content": integration_prompt
            })
            
            # Llamar a la IA
            response = self.ai.chat(messages, integration_prompt)
            
            # Limpiar respuesta
            integrated_code = self._clean_code(response)
            
            return integrated_code if integrated_code else None
            
        except Exception as e:
            # Si falla la integración, retornar None para usar modo overwrite
            return None
    
    def _clean_code(self, code: str) -> str:
        """Limpia el código removiendo bloques markdown si están presentes."""
        # Remover bloques de código markdown
        code = re.sub(r'```[a-z]*\n', '', code)
        code = re.sub(r'```\n?$', '', code)
        code = code.strip()
        return code
