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
    
    # --- 初始化游戏状态 ---
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)
    if 'game_won' not in st.session_state:
        st.session_state.game_won = False

    target = st.session_state.target
    
    # --- 页面主体分为左右两栏 ---
    col1, col2 = st.columns([1, 1])

    # === 左侧：游戏交互区 ===
    with col1:
        st.markdown("### 🎮 猜数字测试区")
        
        # 隐藏谜底，只有猜对了才显示
        if st.session_state.game_won:
            st.success(f"🎉 恭喜你猜对了！目标数字就是 **{target}**！")
        else:
            st.info("❓ 系统生成的目标数字是： **???**")

        # 学生拖动滑块选择数字
        guess = st.slider("滑动选择一个 1-100 的数字来测试", 1, 100, 50, key="slider_guess")
        st.write(f"你当前选择测试的数字是：`{guess}`")
        
        # 重置游戏按钮
        if st.button("🔄 重置并生成新的目标数字"):
            st.session_state.target = random.randint(1, 100)
            st.session_state.game_won = False
            st.session_state.code_template_generated = False
            st.rerun()

    # === 右侧：代码编写与 AI 辅助区 ===
    with col2:
        st.markdown("### 📝 编写逻辑判断代码")
        st.caption("在下方编写 `if/elif/else` 代码，判断 `guess` 和 `target` 的关系。")
        
        # 1. 动态代码提示（点击后才显示完整模板）
        if st.button("💡 我需要代码提示", key="show_template_btn"):
            st.session_state.code_template_generated = True
            
        if 'code_template_generated' in st.session_state and st.session_state.code_template_generated:
            st.markdown("**参考代码框架**：")
            template = (
f"""if guess < target:
    print(f"太小了，你猜的 {{guess}} 比目标数字小")
elif guess > target:
    print(f"太大了，你猜的 {{guess}} 比目标数字大")
else:
    print(f"恭喜你，猜对了！")
"""
            )
            st.code(template, language="python")
        
        # 2. 代码输入框
        user_code = st.text_area(
            "在此处编写你的 Python 代码",
            height=250,
            key="code_input_area"
        )

        # 3. 运行代码逻辑
        if st.button("▶️ 运行我的代码", type="primary"):
            try:
                # 捕获标准输出，这样 print 的内容不会出现在终端，而是显示在页面上
                import io
                from contextlib import redirect_stdout
                
                output_buffer = io.StringIO()
                
                with redirect_stdout(output_buffer):
                    # 将学生的代码放在安全字典中执行，只暴露 guess 和 target
                    exec(user_code, {"guess": guess, "target": target})
                
                # 获取执行后的 print 输出
                execution_output = output_buffer.getvalue()
                
                if execution_output:
                    st.write(f"**代码运行结果：**")
                    st.info(execution_output)
                    
                    # 判断是否猜对，改变游戏状态
                    if "猜对了" in execution_output:
                        st.session_state.game_won = True
                        st.rerun()
                else:
                    st.warning("⚠️ 代码运行了，但没有输出任何结果，请检查你的 print 语句。")
                    
            except Exception as e:
                st.error(f"❌ 代码运行出错啦：{str(e)}")
                st.warning("💡 遇到报错没关系，把错误信息复制到右侧的 AI 智能答疑中，让 AI 帮你看看！")

    # --- 底部 AI 智能答疑模块 ---
    st.markdown("---")
    st.subheader("🤖 AI 智能答疑")
    st.caption("如果代码报错，或者不知道逻辑怎么写，可以直接在下方输入框问 AI。")
    
    ai_question = st.text_input("向 AI 提问...", placeholder="例如：我的 if 语句一直报错怎么办？", key="ai_q_project")
    if ai_question:
        with st.spinner("AI 正在思考中..."):
            try:
                # 调用你之前写好的 OpenAI API 进行回答
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
                openai.api_base = os.getenv("OPENAI_BASE_URL")
                
                response = openai.ChatCompletion.create(
                    model=os.getenv("MODEL"),
                    messages=[
                        {"role": "system", "content": "你是一位耐心、友好的 Python 编程老师。学生正在写猜数字游戏的 if/else 逻辑。如果学生代码报错，不要直接给完整答案，要引导他们思考。"},
                        {"role": "user", "content": f"学生提问：{ai_question}"}
                    ]
                )
                ai_reply = response["choices"][0]["message"]["content"]
                st.markdown(f"**AI 老师回答：**\n{ai_reply}")
            except Exception as e:
                st.error(f"AI 服务暂时无法连接：{str(e)}")