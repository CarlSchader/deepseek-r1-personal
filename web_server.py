import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from pydantic import BaseModel

OPENAI_URL = os.getenv("OPENAI_URL", "http://carlschader.com:8000/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "test-key")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

print(f"OPENAI_URL: {OPENAI_URL}")
print(f"MODEL_NAME: {MODEL_NAME}")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_URL)

app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(message: ChatMessage):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": message.message}],
        stream=True
    )

    async def generate():
        try:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(generate(), media_type="text/event-stream")


