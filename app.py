import streamlit as st
from content import PROJECT_CHALLENGE

# 定义基础知识的课程大纲（恢复之前消失的课程）
BASIC_LESSONS = {
    "第一课：变量与数据类型": "变量是存储数据的容器。例如 x = 10。Python 的基本数据类型包括：整数(int)、浮点数(float)、字符串(str) 和 布尔值(bool)。",
    "第二课：运算符与表达式": "Python 支持算术运算符（+、-、*、/）和比较运算符（==、!=、>、<）。表达式是这些运算符的组合。",
    "第三课：条件判断 (if-elif-else)": "程序可以通过 if-elif-else 语句根据条件执行不同的代码块。注意 Python 使用缩进来表示代码的从属关系。",
    "第四课：循环 (for & while)": "for 循环用于遍历序列（如列表），while 循环在条件为真时不断执行。它们是处理重复任务的利器。",
}

st.title("滨中Python 趣味小课堂")

# 侧边栏导航 (使用下拉菜单以保证兼容所有环境)
menu = ["📖 基础知识", "🎮 综合项目"]
selected = st.sidebar.selectbox("请选择菜单", menu)

if selected == "📖 基础知识":
    st.header("欢迎来到基础学习区")
    st.write("在这里学习 Python 的基础语法和逻辑判断！\n")
    st.divider()

    # 动态生成课程列表
    for title, content in BASIC_LESSONS.items():
        with st.expander(f"📘 {title}", expanded=False):
            st.write(content)
            st.divider()

elif selected == "🎮 综合项目":
    st.subheader(PROJECT_CHALLENGE["title"])
    st.write(PROJECT_CHALLENGE["description"])

    # ---- 查看提示 ----
    if st.button("💡 查看提示"):
        code_text = PROJECT_CHALLENGE["reference_code"]
        with st.expander("👇 点击复制下方的参考代码：", expanded=True):
            st.code(code_text, language="python")

    # ---- 智能答疑 ----
    if st.button("🤖 智能答疑"):
        st.session_state.show_project_chat = True

    if st.session_state.get("show_project_chat", False):
        st.markdown("---")
        st.subheader("🤖 关于本项目的智能答疑")
        st.write("你可以问我：这段代码是什么意思？为什么要用 session_state？怎么修改难度？")

        project_question = st.text_input("输入你的问题：", key="project_q_input")
        if project_question and st.button("发送", key="project_send_btn"):
            try:
                from openai import OpenAI
                client = OpenAI(
                    base_url=st.secrets["OPENAI_BASE_URL"],
                    api_key=st.secrets["OPENAI_API_KEY"],
                )
                context = f"""你是一个耐心的编程老师。学生正在做这个综合项目：
题目：{PROJECT_CHALLENGE['title']}
要求：{PROJECT_CHALLENGE['description']}
参考代码：{PROJECT_CHALLENGE['reference_code']}
学生的问题是：{project_question}
请用简单易懂的语言回答，必要时给出代码示例。"""
                resp = client.chat.completions.create(
                    model=st.secrets.get("OPENAI_MODEL", "glm-4-flash"),
                    messages=[{"role": "user", "content": context}],
                )
                st.success(resp.choices[0].message.content)
            except Exception as e:
                st.error(f"AI 回复失败：{e}")

    st.markdown("---")

    # ---- 游戏初始化 ----
    import random
    if 'secret' not in st.session_state:
        st.session_state.secret = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.message = "游戏开始了！请猜一个 1-100 的数字。"
        st.session_state.show_secret = False  # 确保初始时隐藏答案

    guess = st.slider("请调整滑块选择一个数字：", 1, 100, 50)
    st.write(f"**你当前选择的数字是：{guess}**")

    user_code = st.text_area(
        "✏️ 在这里写你的项目代码（逻辑判断部分）：",
        height=300,
        key="project_code_area",
    )

    if st.button("▶️ 运行/猜数字", type="primary"):
        try:
            safe_globals = {"__builtins__": __builtins__, "st": st, "random": random, "guess": guess}
            exec(user_code, safe_globals)
        except Exception as e:
            st.error(f"❌ 代码运行出错：{e}")

    st.info(st.session_state.message)

    # ---- 猜中后展示隐藏的答案对比模块 ----
    if st.session_state.get("show_secret", False):
        st.markdown("---")
        st.success(f"🎉 **谜底揭晓！** 电脑随机生成的数字正是 **{st.session_state.secret}**！")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="你猜的数字", value=guess)
        with col2:
            st.metric(label="电脑生成的数字", value=st.session_state.secret)
        st.balloons() 

    if st.button("🔄 重置游戏"):
        st.session_state.secret = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.message = "新游戏开始！请猜一个 1-100 的数字。"
        st.session_state.show_secret = False
        st.rerun()