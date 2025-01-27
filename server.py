from vllm import LLM, SamplingParams, PromptType
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

sampling_params = SamplingParams(temperature=0.6)
llm = LLM(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    enforce_eager=True,
    max_model_len=32768,
)

app = FastAPI()


class HealthCheckResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(status="ok")


class Message(BaseModel):
    role: str
    content: str

class PromptRequest(BaseModel):
    model: str
    messages: list[Message]

class GeneratedResult(BaseModel):
    prompt: str | None
    generated_text: str

@app.post("/v1/chat/completions", response_model=list[GeneratedResult])
async def generate(request: PromptRequest):
    # outputs = llm.generate(request.messages, sampling_params)
    outputs = llm.score
    
    results = []
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        results.append(GeneratedResult(prompt=prompt, generated_text=generated_text))
    
    return results

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
