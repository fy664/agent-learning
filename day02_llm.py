import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ===== Tool =====

def get_weather(city: str):
    """查询城市天气"""
    weather_data = {
        "北京": "晴天，25℃",
        "上海": "小雨，22℃",
        "广州": "多云，29℃",
    }

    return weather_data.get(city, f"暂时没有{city}的天气数据")



def get_attractions(city, activity_type):
    """查询城市的景点"""
    attractions_data = {
        "北京": {
            "历史": ["故宫", "长城", "天坛"],
            "自然": ["颐和园", "圆明园"],
        },
        "上海": {
            "历史": ["外滩", "豫园"],
            "自然": ["世纪公园", "滨江森林公园"],
        },
        "广州": {
            "历史": ["陈家祠", "沙面岛"],
            "自然": ["白云山", "越秀公园"],
        },
    }

    city_attractions = attractions_data.get(city, {})
    return city_attractions.get(activity_type, f"暂时没有{city}的{activity_type}景点数据")

def calculate(expression):
    """计算数学表达式"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算错误"
    
def get_transport_cost(city):
    """查询城市的交通费用"""
    transport_cost_data = {
        "北京": 50,
        "上海": 40,
        "广州": 30,
    }

    return transport_cost_data.get(city, f"暂时没有{city}的交通费用数据")
    
# ===== 给 LLM 的工具说明 =====

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "要查询天气的城市",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "需要计算的数学表达式",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_attractions",
            "description": "查询城市的景点",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "要查询景点的城市",
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "活动类型，如历史、自然等",
                    }
                },
                "required": ["city", "activity_type"],
            },
        },
    },
    {
    "type": "function",
    "function": {
        "name": "get_transport_cost",
        "description": "查询指定城市的交通费用",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称",
                }
            },
            "required": ["city"],
        },
    },
},
   
]


# =========================
# Tool registry
# =========================

tool_map = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_attractions": get_attractions,
    "get_transport_cost": get_transport_cost,
   
    
}

# =========================
# Conversation
# =========================

messages = [
    {
        "role": "user",
        "content": """
帮我规划一个北京一日游。

我的预算只有50元。

请查询北京天气、推荐景点、查询交通费用，
然后计算总费用。

如果超过50元，请重新选择更便宜的景点，
直到总费用不超过50元。
""",
    }
]


while True:

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools,
    )

    message = response.choices[0].message

    messages.append(message)

    if not message.tool_calls:
        print(message.content)
        break
    for tool_call in message.tool_calls:

        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print("\n工具调用：", function_name)
        print("参数：", arguments)

        function = tool_map[function_name]

        result = function(**arguments)

        print("工具结果：", result)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )


# =========================
# Second LLM call
# =========================

# final_response = client.chat.completions.create(
#     model="deepseek-v4-flash",
#     messages=messages,
#     tools=tools,
# )

# print("\n最终回答：")
# print(final_response.choices[0].message.content)