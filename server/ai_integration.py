"""
Integración con APIs de IA para generar código y respuestas.
Soporta OpenAI, Anthropic, y modelos locales.
"""
import os
import json
from typing import List, Dict, Optional
import requests


class AIIntegration:
    """Clase para integrar con diferentes proveedores de IA."""
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.api_key = None
        self.base_url = None
        
        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = "https://api.openai.com/v1"
        elif self.provider == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            self.base_url = "https://api.anthropic.com"
        elif self.provider == "ollama":
            self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        elif self.provider == "lmstudio":
            self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234")
    
    def _prepare_messages(self, history: List[Dict], current_query: str, system_prompt: Optional[str] = None) -> List[Dict]:
        """Prepara los mensajes para la API de IA."""
        messages = []
        
        # System prompt por defecto
        if not system_prompt:
            system_prompt = """Eres un asistente de programación experto. Ayudas a escribir código, debuggear, explicar conceptos y crear soluciones.

Cuando el usuario te pida crear o modificar código:
1. Responde de forma clara y concisa
2. Si es código, inclúyelo en bloques de código markdown
3. Sé específico y práctico
4. Si el usuario quiere que escribas código en un archivo, proporciona el código completo y listo para usar"""
        
        messages.append({"role": "system", "content": system_prompt})
        
        # Añadir historial
        for msg in history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Añadir consulta actual
        messages.append({"role": "user", "content": current_query})
        
        return messages
    
    def chat(self, history: List[Dict], query: str) -> str:
        """Envía una consulta a la IA y retorna la respuesta."""
        messages = self._prepare_messages(history, query)
        
        if self.provider == "openai":
            return self._chat_openai(messages)
        elif self.provider == "anthropic":
            return self._chat_anthropic(messages)
        elif self.provider == "ollama":
            return self._chat_ollama(messages)
        elif self.provider == "lmstudio":
            return self._chat_lmstudio(messages)
        else:
            return "Error: Proveedor de IA no configurado correctamente"
    
    def _chat_openai(self, messages: List[Dict]) -> str:
        """Chat con OpenAI API."""
        if not self.api_key:
            return "Error: OPENAI_API_KEY no configurada en .env"
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except ImportError:
            return "Error: Instala openai con 'pip install openai'"
        except Exception as e:
            return f"Error al conectar con OpenAI: {str(e)}"
    
    def _chat_anthropic(self, messages: List[Dict]) -> str:
        """Chat con Anthropic Claude API."""
        if not self.api_key:
            return "Error: ANTHROPIC_API_KEY no configurada en .env"
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Anthropic usa formato diferente
            system_msg = messages[0]["content"] if messages[0]["role"] == "system" else ""
            conversation = [msg for msg in messages[1:] if msg["role"] != "system"]
            
            response = client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
                max_tokens=2000,
                system=system_msg,
                messages=conversation
            )
            
            return response.content[0].text
        except ImportError:
            return "Error: Instala anthropic con 'pip install anthropic'"
        except Exception as e:
            return f"Error al conectar con Anthropic: {str(e)}"
    
    def _chat_ollama(self, messages: List[Dict]) -> str:
        """Chat con Ollama (modelo local)."""
        try:
            # Convertir mensajes a formato Ollama
            prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    prompt += f"System: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    prompt += f"User: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    prompt += f"Assistant: {msg['content']}\n\n"
            
            prompt += "Assistant:"
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": os.getenv("OLLAMA_MODEL", "llama2"),
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "Error: No response from Ollama")
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"Error al conectar con Ollama: {str(e)}"
    
    def _chat_lmstudio(self, messages: List[Dict]) -> str:
        """Chat con LM Studio (modelo local)."""
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": os.getenv("LMSTUDIO_MODEL", "local-model"),
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: LM Studio returned status {response.status_code}"
        except Exception as e:
            return f"Error al conectar con LM Studio: {str(e)}"
    
    def generate_code(self, query: str, history: List[Dict], file_path: Optional[str] = None) -> Dict:
        """
        Genera código basado en una consulta y opcionalmente lo escribe en un archivo.
        Retorna: {"code": código, "explanation": explicación, "file_path": ruta}
        """
        # Preparar prompt específico para generación de código
        code_prompt = f"""El usuario quiere generar código. 

Consulta: {query}
{"Archivo objetivo: " + file_path if file_path else ""}

Responde SOLO con un JSON válido en este formato:
{{
    "code": "el código completo aquí",
    "explanation": "breve explicación de lo que hace el código",
    "language": "python/javascript/etc"
}}

Si el usuario no especifica un archivo pero quiere código, proporciona el código de todas formas.
Si el usuario quiere código en un archivo específico, inclúyelo en la respuesta."""
        
        messages = self._prepare_messages(history, code_prompt)
        response = self.chat(messages, code_prompt)
        
        # Intentar extraer JSON de la respuesta
        try:
            # Buscar JSON en la respuesta
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                code_data = json.loads(json_match.group())
                return code_data
            else:
                # Si no hay JSON, asumir que toda la respuesta es código
                return {
                    "code": response,
                    "explanation": "Código generado por IA",
                    "language": "python"
                }
        except:
            # Si falla el parsing, retornar respuesta completa como código
            return {
                "code": response,
                "explanation": "Respuesta de IA",
                "language": "text"
            }
