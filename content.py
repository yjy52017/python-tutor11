LESSONS = [
    {
        "id": 1,
        "title": "第一课：你好，Python！",
        "concept": "print() 函数用来在屏幕上输出内容。试试打印一句问候语吧！",
        "hint": 'print("你好，Python！")',
        "task": "请使用 print() 输出：你好，Python！",
        "expected": "你好，Python！",
    },
    {
        "id": 2,
        "title": "第二课：变量与数据类型",
        "concept": "变量就像一个盒子，可以存放数据。Python 常见类型有：整数(int)、小数(float)、字符串(str)。",
        "hint": 'name = "小明"\nage = 16\nprint(name, age)',
        "task": "定义一个变量 name 赋值为你的名字，再定义一个变量 age 赋值为你的年龄，然后打印它们。",
        "expected": None,
    },
    {
        "id": 3,
        "title": "第三课：if 条件判断",
        "concept": "if 语句让程序根据不同条件执行不同代码。注意 Python 用缩进来表示代码块！",
        "hint": 'score = 85\nif score >= 60:\n    print("及格了")\nelse:\n    print("没及格")',
        "task": "定义变量 score = 75，如果 score >= 60 输出及格，否则输出不及格。",
        "expected": "及格",
    },
    {
        "id": 4,
        "title": "第四课：for 循环",
        "concept": "for 循环可以重复执行一段代码。range(5) 会生成 0,1,2,3,4。",
        "hint": "for i in range(5):\n    print(i)",
        "task": "使用 for 循环打印数字 1 到 5。",
        "expected": "1\n2\n3\n4\n5",
    },
    {
        "id": 5,
        "title": "第五课：函数定义",
        "concept": "函数是一段可复用的代码，用 def 关键字定义。",
        "hint": 'def greet(name):\n    return "你好，" + name\n\nprint(greet("Python"))',
        "task": "定义一个函数 add(a, b)，返回两个数的和。然后调用 add(3, 5) 并打印结果。",
        "expected": "8",
    },
]

PROJECT_CHALLENGE = {
    "title": "小项目：猜数字游戏",
    "description": """电脑随机生成一个 1~100 的数字，玩家来猜。每次猜完告诉玩家大了或小了，直到猜中为止。

提示：
- 用 import random 和 random.randint(1, 100) 生成随机数
- 用 while 循环让玩家反复猜
- 用 if/elif/else 判断大小""",
    "reference_code": """import random

number = random.randint(1, 100)
count = 0

while True:
    guess = int(input("猜一个1-100的数字："))
    count += 1
    if guess < number:
        print("小了！")
    elif guess > number:
        print("大了！")
    else:
        print(f"恭喜！你用了{count}次猜中了！")
        break""",
}