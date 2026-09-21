name = input("请输入你的名字：")
age = int(input("请输入你的年龄："))

print(f"你好，{name}！")
print(f"你今年 {age} 岁。")
print(f"明年你就 {age + 1} 岁了。")

if age >= 18:
    print("你已经成年。")
else:
    print("你还未成年。")