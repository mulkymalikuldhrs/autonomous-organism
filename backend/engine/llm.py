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
        if "ESTIMATE SAAS POTENTIAL" in prompt_upper:
            return """
AUTOMATION_EASE: 0.85
REVENUE_POTENTIAL: 0.75
MARKET_GAP: 0.90
THEME: Automated Customer Support for Niche E-commerce
SUMMARY: A streamlined AI support agent specifically tuned for small shop owners who cannot afford full-time staff but have high ticket volume.
"""

        # SaaS Factory Fallback
        if "TECHNICAL SPECIFICATION" in prompt_upper:
            return json.dumps({
                "db_schema": ["users", "tickets", "replies"],
                "endpoints": ["GET /api/tickets", "POST /api/tickets/resolve"],
                "features": ["AI Auto-reply", "Sentiment dashboard", "Email integration"],
                "stack": {"backend": "FastAPI", "frontend": "React/Vite/Tailwind", "db": "SQLite"}
            })

        if "THEME:" in prompt_upper or "BLUEPRINT" in prompt_upper:
            return """
THEME: AI-Powered Micro-SaaS for Niche Problem
SCORE: 85
SUMMARY: An automated solution that solves specific pain points identified in recent community discussions.
SCHEMA: {"tables": ["users", "tasks", "analytics"]}
ENDPOINTS: ["GET /api/status", "POST /api/action"]
FRONTEND_COMPONENTS: ["Dashboard", "ActionPanel", "StatsView"]
"""
        if "POST" in prompt_upper or "PROMO" in prompt_upper:
            return "🚀 Excited to launch our new autonomous solution! Check it out and solve your problems today. #SaaS #Automation"

        return "Autonomous SaaS Organism is currently offline but thinking deeply about your request."

llm = LLMInterface()
