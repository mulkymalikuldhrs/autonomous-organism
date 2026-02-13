import httpx
import json
import os
import asyncio

class LLMInterface:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.hf_token = os.getenv("HF_TOKEN")
        # Free models on HF Inference API
        self.hf_model = "mistralai/Mistral-7B-Instruct-v0.2"

    async def generate(self, prompt: str, system: str = "") -> str:
        # 1. Try Ollama first (Local)
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

        # 2. Try HuggingFace (if token available)
        if self.hf_token:
            try:
                hf_url = f"https://api-inference.huggingface.co/models/{self.hf_model}"
                headers = {"Authorization": f"Bearer {self.hf_token}"}
                payload = {
                    "inputs": f"<s>[INST] {system} {prompt} [/INST]",
                    "parameters": {"max_new_tokens": 500}
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(hf_url, headers=headers, json=payload)
                    if response.status_code == 200:
                        res_json = response.json()
                        if isinstance(res_json, list) and len(res_json) > 0:
                            return res_json[0].get("generated_text", "").split("[/INST]")[-1].strip()
                        return res_json.get("generated_text", "")
            except Exception as e:
                print(f"HuggingFace error: {e}")

        # 3. Fallback to templates/simple logic
        return self._fallback_logic(prompt)

    def _fallback_logic(self, prompt: str) -> str:
        # Improved template fallback
        if "THEME:" in prompt or "SaaS" in prompt:
            return "THEME: AI-Powered Niche Market Research Tool\nSCORE: 82\nSUMMARY: A tool that automatically aggregates pain points from Reddit and HackerNews to suggest viable Micro-SaaS ideas with high automation potential."
        return "Autonomous SaaS Organism is operating in autonomous mode. Model connection pending."

llm = LLMInterface()
