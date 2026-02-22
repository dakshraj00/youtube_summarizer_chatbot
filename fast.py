from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot_back import model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["hhttp://localhost:8501/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    type: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    config: dict

@app.post("/run")
async def run_chat(req: ChatRequest):
    messages = [m.content for m in req.messages]
    result = model.invoke({"messages": messages}, config=req.config)
    reply = result["messages"][-1].content
    return {"output": reply}

