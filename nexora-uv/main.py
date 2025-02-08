from fastapi import FastAPI
from dotenv import load_dotenv
from api import chat, steam

# Load environment variables
load_dotenv()

app = FastAPI()

# Include routers
app.include_router(chat.router)
app.include_router(steam.router)

@app.get("/")
def read_root():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)