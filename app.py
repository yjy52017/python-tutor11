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

    # 1. 初始化游戏状态（只在第一次打开或重置时执行）
    if 'secret' not in st.session_state:
        st.session_state.secret = random.randint(1, 100)
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'is_over' not in st.session_state:
        st.session_state.is_over = False

    # 2. 显示提示和结果
    if st.session_state.message:
        st.success(st.session_state.message)
    
    st.text_input("请输入你猜的数字（1-100）", key="guess_input")

    # 3. 定义猜数字的逻辑函数（绑定给按钮触发）
    def guess_number():
        try:
            user_guess = int(st.session_state.guess_input)
            st.session_state.count += 1
            
            if st.session_state.is_over:
                st.session_state.message = "游戏已结束，请重置后再玩。"
            elif user_guess == st.session_state.secret:
                st.session_state.message = f"🎉 恭喜你！你用了 {st.session_state.count} 次猜中了！"
                st.session_state.is_over = True
            elif user_guess < st.session_state.secret:
                st.session_state.message = f"你猜的 {user_guess} 小了！请继续猜。"
            else:
                st.session_state.message = f"你猜的 {user_guess} 大了！请继续猜。"
        except ValueError:
            st.session_state.message = "请输入一个有效的整数哦！"
        # 猜完清空输入框，准备下一次
        st.session_state.guess_input = ""

    # 4. 定义重置游戏的逻辑
    def restart_game():
        st.session_state.secret = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.message = ""
        st.session_state.is_over = False
        st.session_state.guess_input = ""

    # 5. 放置按钮
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("🔄 重置游戏", on_click=restart_game)
    with col2:
        st.button("▶️ 猜数字", on_click=guess_number, type="primary")

    # 6. 游戏结束时揭晓谜底
    if st.session_state.is_over:
        st.info(f"🎉 谜底揭晓！电脑随机生成的数字正是 **{st.session_state.secret}**！")
        st.metric(label="你猜对的数字", value=st.session_state.guess_input if st.session_state.guess_input else "已猜中")
        st.metric(label="电脑生成的数字", value=st.session_state.secret)