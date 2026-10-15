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