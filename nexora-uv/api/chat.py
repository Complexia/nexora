import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
import httpx
import json

# Add at the very top of the file
print("Current working directory:", os.getcwd())
print("Does .env exist?:", os.path.exists(".env"))
load_dotenv()


router = APIRouter(prefix="/chat")

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
grok_api_key = os.getenv("XAI_API_KEY")

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"  # default model

async def stream_openai_response(message: str, model: str):
    # ... existing code ...
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def stream_grok_response(message: str):
    # ... existing code ...
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {grok_api_key}"
                },
                json={
                    "messages": [
                        {"role": "user", "content": message}
                    ],
                    "model": "grok-2-latest",
                    "stream": True
                },
                timeout=60.0
            )
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data != "[DONE]":
                        try:
                            chunk = json.loads(data)
                            if content := chunk.get("choices", [{}])[0].get("delta", {}).get("content"):
                                yield content
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def chat(request: ChatRequest):
    if request.model.lower().startswith("grok"):
        stream = stream_grok_response(request.message)
    else:
        stream = stream_openai_response(request.message, request.model)
    
    return StreamingResponse(
        stream,
        media_type="text/event-stream"
    ) 