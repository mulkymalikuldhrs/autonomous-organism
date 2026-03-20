import httpx
import json
import os

class LLMInterface:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.hf_token = os.getenv("HF_TOKEN")
        self.hf_model = "mistralai/Mistral-7B-Instruct-v0.2"

    async def generate(self, prompt: str, system: str = "") -> str:
        # 1. Try Ollama (Local)
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

        # 2. Try HuggingFace (Cloud Free API)
        if self.hf_token:
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"https://api-inference.huggingface.co/models/{self.hf_model}",
                        headers={"Authorization": f"Bearer {self.hf_token}"},
                        json={"inputs": f"{system}\n\n{prompt}" if system else prompt}
                    )
                    if response.status_code == 200:
                        res_json = response.json()
                        # HF sometimes returns a list of objects
                        if isinstance(res_json, list) and len(res_json) > 0:
                            output = res_json[0].get("generated_text", "")
                        else:
                            output = res_json.get("generated_text", "")

                        # Clean up if the model echoes the prompt
                        if output.startswith(f"{system}\n\n{prompt}" if system else prompt):
                            output = output[len(f"{system}\n\n{prompt}" if system else prompt):].strip()
                        return output
            except Exception as e:
                print(f"HuggingFace error: {e}")

        # 3. Fallback to templates
        return self._fallback_logic(prompt)

    def _fallback_logic(self, prompt: str) -> str:
        prompt_upper = prompt.upper()

        # Decision Core Fallback
        if "AUTOMATION_EASE" in prompt_upper or "REVENUE_POTENTIAL" in prompt_upper:
            return """
AUTOMATION_EASE: 0.85
REVENUE_POTENTIAL: 0.75
MARKET_GAP: 0.90
THEME: Autonomous Niche Analyzer
SUMMARY: A specialized tool that automatically identifies and analyzes underserved market niches using real-time community data.
"""

        # SaaS Factory Fallback
        if "DB_SCHEMA" in prompt_upper or "ENDPOINTS" in prompt_upper or "FEATURES" in prompt_upper:
            return """
{
  "db_schema": ["users", "analyses", "settings"],
  "endpoints": ["GET /api/health", "POST /api/analyze", "GET /api/results"],
  "features": ["Real-time data scraping", "Automated sentiment analysis", "Revenue potential estimation"],
  "stack": {"backend": "FastAPI", "frontend": "React/Vite/Tailwind", "db": "SQLite"}
}
"""

        # Growth Engine Fallback
        if "POST" in prompt_upper or "PROMO" in prompt_upper or "LAUNCH" in prompt_upper:
            return "🚀 Excited to announce our latest autonomous innovation! Solving real-world problems with Zero-Cost infrastructure. #AutonomousOrganism #SaaS #Growth"

        return "Autonomous SaaS Organism (Gen-4) is processing your request in deep-thought mode. Implementation pending."

llm = LLMInterface()
