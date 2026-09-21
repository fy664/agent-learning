import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from app.agent import run_agent
from fastapi import UploadFile, File, Form

# 加载环境变量
load_dotenv()


# 创建 FastAPI 应用
app = FastAPI(
    title="AI Agent API",
    description="My first AI Agent backend",
    version="1.0.0"
)


# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# 定义请求格式
class ChatRequest(BaseModel):
    message: str


# 首页测试接口
@app.get("/")
def home():
    return {
        "message": "Hello AI Full Stack"
    }


# AI聊天接口
@app.post("/chat")
async def chat(
    message: str = Form(...),
    image: UploadFile = File(None)
):

    if image:
        print("收到图片:", image.filename)

    return {
        "answer": "收到你的消息"
    }