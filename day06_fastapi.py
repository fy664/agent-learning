import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Hello AI Full Stack"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "你是一个友好、简洁的 AI 助手。",
            },
            {
                "role": "user",
                "content": request.message,
            },
        ],
    )

    return {
        "answer": response.choices[0].message.content
    }