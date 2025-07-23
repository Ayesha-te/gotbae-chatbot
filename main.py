from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
@app.get("/uptime")
def ping():
    return {"ping": "pong", "status": "alive"}


# CORS for frontend (Vercel)
app.add_middleware(
    CORSMiddleware,
     allow_origins=["https://gotbae-dma.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load chatbot prompt (ask me if you want to hardcode instead)
with open("gotbae_chatbot_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Schema for input
class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: ChatInput):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
