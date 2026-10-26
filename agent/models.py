from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

model = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0,
)



