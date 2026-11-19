from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from openai import OpenAI
from api.core.config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_llm(provider, model_name, messages, reasoning_effort="minimal", max_tkens=500):
    if provider == "openai":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tkens,
            reasoning_effort=reasoning_effort
        )
        return response.choices[0].message.content

class ChatRequest(BaseModel):
    provider: str
    model_name: str
    messages: list[dict]

class ChatResponse(BaseModel):
    message: str

app = FastAPI()
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = run_llm(
            provider=request.provider,
            model_name=request.model_name,
            messages=request.messages
        )
        return ChatResponse(message=result)
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {e}")
        return Response(content=str(e), status_code=500)