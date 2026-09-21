# ===== Tool Functions =====


def get_weather(city: str):
    """查询城市天气"""
    weather_data = {
        "北京": "晴天，25℃",
        "上海": "小雨，22℃",
        "广州": "多云，29℃",
    }

    return weather_data.get(
        city,
        f"暂时没有{city}的天气数据"
    )


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

    return city_attractions.get(
        activity_type,
        f"暂时没有{city}的{activity_type}景点数据"
    )


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

    return transport_cost_data.get(
        city,
        f"暂时没有{city}的交通费用数据"
    )


# ===== Tool Registry =====

tool_map = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_attractions": get_attractions,
    "get_transport_cost": get_transport_cost,
}
