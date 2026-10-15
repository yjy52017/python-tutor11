import streamlit as st
import random
import os
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL
from content import LESSONS, PROJECT_CHALLENGE

st.set_page_config(page_title="Python自学助手", page_icon="🐍", layout="wide")

st.title("🐍 樟树市滨江中学高一学生自学Python编程AI助手")
st.markdown("---")

st.sidebar.header("📚 课程目录")
selected = st.sidebar.radio("选择课程", [l["title"] for l in LESSONS] + ["🎮 综合项目"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

lesson = None
if selected != "🎮 综合项目":
    for l in LESSONS:
        if l["title"] == selected:
            lesson = l
            break

if lesson:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(lesson["title"])
        st.info(lesson["concept"])
        st.markdown("### 📝 任务")
        st.write(lesson["task"])
        with st.expander("💡 看提示"):
            st.code(lesson["hint"], language="python")

        user_code = st.text_area(
            "✏️ 在这里写代码",
            value=lesson["hint"],
            height=200,
            key=f"code_{lesson['id']}",
        )

        if st.button("▶️ 运行代码", type="primary"):
            try:
                exec(user_code, {})
                st.success("✅ 代码运行完成！")
                if lesson["expected"]:
                    st.write("期望输出：", lesson["expected"])
            except Exception as e:
                st.error(f"❌ 运行出错：{e}")

    with col2:
        st.subheader("🤖 智能答疑")
        st.markdown("遇到不懂的地方？直接问我！")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("输入你的问题..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            context = (
                "你是一位耐心友好、擅长教高中生的Python老师。"
                f"当前学生正在学习：{lesson['title']}。"
                f"知识点：{lesson['concept']}。"
                f"任务：{lesson['task']}。"
                f"学生代码：{user_code}。"
                "请用简单易懂的语言回答，必要时给出代码示例。"
            )

            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": prompt},
                    ],
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ AI服务暂时不可用：{e}"

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

elif selected == "🎮 综合项目":
    st.subheader(PROJECT_CHALLENGE["title"])
    st.write(PROJECT_CHALLENGE["description"])

    # 1. 系统初始化一个目标数字
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)

    # 2. 左侧交互区：猜数字
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎮 猜数字测试")
        st.info(f"系统生成的目标数字是：**{st.session_state.target}**")
        
        guess = st.slider("滑动选择一个 1-100 的数字来测试", 1, 100, 50)
        st.write(f"你选择测试的数字是：`{guess}`")

    # 3. 右侧代码区：编写逻辑
    with col2:
        st.markdown("### 📝 编写逻辑判断代码")
        
        # 预设代码框架
        template = (
            "# 目标数字是 target = " + str(st.session_state.target) + "\n"
            "# 测试数字是 guess = " + str(guess) + "\n"
            "# 请在这里编写你的 if/else 判断逻辑：\n\n"
            "# if guess < target:\n"
            "#     ...\n"
        )

        code_input = st.text_area(
            "在此处编写代码",
            value=template,
            height=250,
            key="code_input"
        )

        if st.button("▶️ 运行我的代码"):
            try:
                target = st.session_state.target
                # 执行学生写的代码
                exec(code_input, {"target": target, "guess": guess, "print": st.write})
            except Exception as e:
                st.error(f"❌ 代码运行出错：{e}")

    # 4. 重新生成题目的按钮
    st.markdown("---")
    if st.button("🔄 重置并生成新的目标数字"):
        st.session_state.target = random.randint(1, 100)
        st.rerun()