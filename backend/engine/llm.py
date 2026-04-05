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

        # Enhanced Multi-stage Fallback for 'Decision'
        if "THEME:" in prompt_upper or "CHOOSE THE BEST" in prompt_upper:
            return json.dumps({
                "AUTOMATION_EASE": 90,
                "REVENUE_POTENTIAL": 85,
                "MARKET_GAP": 75,
                "THEME": "AI-Driven Customer Feedback Analyzer",
                "SUMMARY": "A tool that automatically categorizes and summarizes customer feedback from multiple channels using LLMs."
            })

        # Enhanced Multi-stage Fallback for 'Factory'
        if "BLUEPRINT" in prompt_upper or "DB_SCHEMA" in prompt_upper:
            return json.dumps({
                "db_schema": {
                    "tables": ["feedback_raw", "feedback_clean", "insights", "users"]
                },
                "endpoints": [
                    "POST /api/ingest",
                    "GET /api/insights",
                    "GET /api/status"
                ],
                "features": [
                    "Multi-source ingestion",
                    "LLM-based categorization",
                    "Real-time dashboard"
                ]
            })

        if "POST" in prompt_upper or "PROMO" in prompt_upper:
            return "🚀 Excited to launch our new autonomous solution! Check it out and solve your problems today. #SaaS #Automation #Gen4"

        return "Autonomous SaaS Organism is currently offline but thinking deeply about your request."

llm = LLMInterface()
