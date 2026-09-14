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
    
 

    state["tool_results"].append(transport_cost_data.get(city, f"暂时没有{city}的交通费用数据"))
    return transport_cost_data.get(city, f"暂时没有{city}的交通费用数据")
    
def run_agent(state, tools, tool_map):
     
    max_iterations = 5

    for i in range(max_iterations):

        print(f"\n===== Agent Iteration {i + 1} =====")

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=state["messages"],
            tools=tools,
        )

        message = response.choices[0].message

        state["messages"].append(message)

        # LLM 不再需要调用工具
        if not message.tool_calls:
            return message.content

        # 处理本轮所有 Tool Call
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name
            arguments = json.loads(
                tool_call.function.arguments
            )

            print("工具调用：", function_name)
            print("参数：", arguments)

            function = tool_map.get(function_name)

            if function is None:
                tool_result = f"不存在的工具：{function_name}"

            else:
                try:
                    tool_result = function(**arguments)
                except Exception as e:
                    tool_result = f"工具执行失败：{e}"

            print("工具结果：", tool_result)

            state["messages"].append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result),
                }
            )
            state["tool_results"].append(
                {
                    "tool_call_id": function_name,
                    "result": tool_result,
                }
            )
        
    state["final_answer"] = "Agent 达到最大迭代次数，任务未完成。"
    return state["final_answer"]   
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

state = {
    "messages": [
        {
            "role": "user",
            "content": "帮我规划一个北京一日游。\n\n预算只有100元。"
        }
    ],
    "user_goal": "",
    "iteration": 0,
    "tool_results": [],
    "final_answer": None,
}

messages = state["messages"]

tool_results = state["tool_results"]

final_result = run_agent(
    state=state,
    tools=tools,
    tool_map=tool_map
)

print("\n===== 最终回答 =====")
print(final_result)
print("\n===== Agent State =====")
print(state)





