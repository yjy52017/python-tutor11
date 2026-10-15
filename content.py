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
    "title": "小项目：猜数字游戏（网页版）",
    "description": """电脑随机生成一个 1~100 的数字，玩家来猜。
    
注意：因为滑块（guess）和游戏初始化（secret, count）已经由系统提供，
你只需要在下方编写**逻辑判断代码**即可。""",
    "reference_code": """st.session_state.count += 1

if guess < st.session_state.secret:
    st.session_state.message = f"{guess} 小了！请继续猜。"
elif guess > st.session_state.secret:
    st.session_state.message = f"{guess} 大了！请继续猜。"
else:
    st.session_state.message = f"恭喜你！你用了 {st.session_state.count} 次猜中了！🎉"
    st.session_state.show_secret = True  # 新增：猜中后显示答案
    st.session_state.secret = random.randint(1, 100)
    st.session_state.count = 0""",
}