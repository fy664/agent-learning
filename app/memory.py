# ===== Memory =====

memory = {
    "name": None,
    "likes": [],
    "learning": [],
}


def update_memory(user_input):
    """根据用户输入更新 Memory"""

    if user_input.startswith("我叫"):
        memory["name"] = user_input[2:]


def get_memory():
    """获取当前 Memory"""
    return memory
