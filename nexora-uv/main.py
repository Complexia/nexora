from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"  # default model

async def stream_openai_response(message: str, model: str):
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

@app.post("/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(
        stream_openai_response(request.message, request.model),
        media_type="text/event-stream"
    )

# Keep the root endpoint for health check
@app.get("/")
def read_root():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)