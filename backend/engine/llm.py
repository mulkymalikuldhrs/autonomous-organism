import httpx
import json
import os

class LLMInterface:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.hf_token = os.getenv("HF_TOKEN")

    async def generate(self, prompt: str, system: str = "") -> str:
        # Try Ollama first
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json={
                        "model": "llama3",
                        "prompt": f"{system}\n\n{prompt}" if system else prompt,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")

        # Fallback to templates/simple logic if Ollama fails
        return self._fallback_logic(prompt)

    def _fallback_logic(self, prompt: str) -> str:
        # Very basic fallback
        if "THEME:" in prompt:
            return "THEME: Micro-SaaS for Task Management\nSCORE: 75\nSUMMARY: A simple task manager for remote teams."
        return "Autonomous SaaS Organism is thinking..."

llm = LLMInterface()
