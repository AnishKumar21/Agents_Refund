
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from deepeval.models import DeepEvalBaseLLM
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

class GroqEvalModel(DeepEvalBaseLLM):
    def __init__(self):
        self.model = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return str(response.content)

    async def a_generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)
        return str(response.content)

    def get_model_name(self) -> str:
        return "Groq GPT-OSS 120B"

eval_model = GroqEvalModel()
