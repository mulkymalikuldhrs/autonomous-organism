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
        if "AUTOMATION_EASE" in prompt_upper and "REVENUE_POTENTIAL" in prompt_upper:
            options = [
                {
                    "theme": "Sistem Manajemen Stok Otomatis UMKM",
                    "summary": "Platform otonom untuk membantu UMKM melacak stok barang dan memberikan prediksi kapan harus belanja lagi berdasarkan tren penjualan lokal.",
                    "auto": 0.82, "rev": 0.88, "gap": 0.75
                },
                {
                    "theme": "AI-Powered Autonomous Content Manager",
                    "summary": "A system that automatically identifies content gaps in niche markets and generates SEO-optimized articles and social media posts.",
                    "auto": 0.85, "rev": 0.75, "gap": 0.90
                },
                {
                    "theme": "Monitor Keluhan Publik Otomatis",
                    "summary": "Sistem yang memantau media sosial untuk keluhan publik tentang layanan infrastruktur dan merangkumnya untuk pihak terkait.",
                    "auto": 0.78, "rev": 0.65, "gap": 0.85
                }
            ]
            import random
            chosen = random.choice(options)
            return f"""
AUTOMATION_EASE: {chosen['auto']}
REVENUE_POTENTIAL: {chosen['rev']}
MARKET_GAP: {chosen['gap']}
THEME: {chosen['theme']}
SUMMARY: {chosen['summary']}
"""

        # Factory Fallback
        if "DB_SCHEMA" in prompt_upper or "ENDPOINTS" in prompt_upper:
            return json.dumps({
                "db_schema": ["users", "contents", "analytics", "subscriptions", "settings"],
                "endpoints": ["GET /api/status", "POST /api/sync", "GET /api/data", "POST /api/settings"],
                "features": ["Neural Grid Sync", "Autonomous Scraper", "LLM Content Generator", "Auto-scheduler"],
                "ui_ux_strategy": "Bioluminescent Edition with deep slate backgrounds, cyan neon accents, and smooth neural-style transitions.",
                "monetization_model": "Freemium model with subscription for advanced autonomous sub-routines and API access.",
                "stack": {"backend": "FastAPI", "frontend": "React/Vite/Tailwind", "db": "SQLite"}
            })

        # Growth Fallback
        if "POST" in prompt_upper or "PROMO" in prompt_upper:
            return "🚀 Excited to launch our new autonomous solution! Check it out and solve your problems today. #SaaS #Automation #OpenSource"

        return "Autonomous SaaS Organism is currently offline but thinking deeply about your request."

llm = LLMInterface()
