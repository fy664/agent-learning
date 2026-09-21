from app.llm import chat
from app.tools import get_weather, calculate


tools = {
    "get_weather": get_weather,
    "calculate": calculate
}


def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content":
            """
            你是一个扫furry。
            如果需要外部信息，
            可以调用工具。
            """
        },
        {
            "role": "user",
            "content": user_input
        }
    ]


    response = chat(messages)


    return response