import streamlit as st
import os
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL
from content import LESSONS, PROJECT_CHALLENGE

st.set_page_config(page_title="Python自学助手", page_icon="🐍", layout="wide")

st.title("🐍 樟树市滨江中学高一Python自学助手")
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
    
    # 1. 全局初始化游戏状态（确保游戏始终能运行）
    import random
    if 'secret' not in st.session_state:
        st.session_state.secret = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.message = "游戏开始了！请猜一个 1-100 的数字。"

    # 2. 提供滑动条（学生无需再写这行，直接使用即可）
    guess = st.slider("请调整滑块选择一个数字：", 1, 100, 50)
    st.markdown("---")
    st.write(f"**你当前选择的数字是：{guess}**")
    
    # 3. 学生的代码区域
    user_code = st.text_area(
        "✏️ 在这里写你的项目代码（逻辑判断部分）：", 
        height=300,
        key="project_code_area"
    )
    
    # 4. 运行逻辑（把你的代码和学生的代码融合）
    if st.button("▶️ 运行/猜数字", type="primary"):
        try:
            # 准备一个安全的执行环境，并自动引入必要的模块
            safe_globals = {"__builtins__": __builtins__, "st": st, "random": random, "guess": guess}
            # 执行学生写的代码
            exec(user_code, safe_globals)
            # 如果学生没有改变 message，则显示默认成功提示
            if st.session_state.message == "游戏开始了！请猜一个 1-100 的数字。":
                st.session_state.message = "请点击按钮猜数字，或者修改你的代码！"
        except Exception as e:
            st.error(f"❌ 代码运行出错：{e}")

    # 5. 显示反馈结果
    st.info(st.session_state.message)
    
    # 6. 重置游戏按钮
    if st.button("🔄 重置游戏（重新生成随机数）"):
        st.session_state.secret = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.message = "新游戏开始！请猜一个 1-100 的数字。"
        st.rerun()