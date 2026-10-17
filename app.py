import streamlit as st
import random
import os
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL
from content import LESSONS, PROJECT_CHALLENGE

# --- 图片路径安全获取逻辑 ---
# 获取当前 app.py 所在的目录，确保云端和本地都能准确找到图片
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")
icon_path = os.path.join(current_dir, "logo.png") if os.path.exists(os.path.join(current_dir, "logo.png")) else "🐍"

# --- 页面基础配置 ---
st.set_page_config(
    page_title="滨中Python自学助手",
    page_icon=icon_path,  # 浏览器标签页的小图标，如果没有图片则自动回退到蛇
    layout="wide"
)

# 页面头部布局：左侧Logo + 右侧标题
col_logo, col_title = st.columns([1, 10])
with col_logo:
    # 安全判断：如果云端成功找到图片就显示，找不到则不报错
    if os.path.exists(logo_path):
        st.image(logo_path, width=120) 
with col_title:
    st.title("高一学生自学Python编程AI助手")
st.markdown("---")

# 侧边栏 Logo
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    st.header("📚 课程目录")

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
            value="",
            height=200,
            key=f"code_{lesson['id']}",
        )

        # 注意：这里没有多余的空格，完美缩进
        if st.button("▶️ 运行代码", type="primary"):
            import io
            from contextlib import redirect_stdout
            
            # 创建一个“虚拟屏幕”来接收 print 的输出
            output_buffer = io.StringIO()
            try:
                # 运行学生代码，并将 print 的内容重定向到虚拟屏幕
                with redirect_stdout(output_buffer):
                    exec(user_code, {})
                
                # 提取实际输出，并去除首尾空格
                actual_output = output_buffer.getvalue().strip()
                # 获取 content.py 里的期望答案
                expected_output = lesson.get("expected")

                # 1. 显示学生自己代码的实际输出
                if actual_output:
                    st.info(f"**你的代码输出：** `{actual_output}`")
                else:
                    st.warning("⚠️ 你的代码运行了，但没有看到任何输出（请检查 print 语句）。")

                # 2. 自动判题（对比实际输出和期望输出）
                if expected_output is not None:
                    if actual_output == expected_output.strip():
                        st.success("✅ 太棒了！输出结果完全正确！🎉")
                    else:
                        st.error("❌ 运行完成，但输出结果不对哦。")
                        st.warning(f"**期望输出：** `{expected_output}`")
                        st.caption("💡 提示：请仔细检查输出内容、空格以及标点符号（请使用英文半角）。")
                        
            except Exception as e:
                st.error(f"❌ 代码运行报错啦：\n`{e}`")
                st.caption("💡 提示：请检查括号、引号是否闭合，缩进是否正确。")

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

            # 注意：这里完美对齐，没有多余的缩进
            context = (
                "你是一位耐心友好、擅长教高中生的Python老师。"
                f"当前学生正在学习：{lesson['title']}。"
                f"知识点：{lesson.get('concept', 'Python基础编程')}。"
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
    st.caption("遇到不懂的地方？直接问我！")

    # 初始化历史记录
    if "chat_history_project" not in st.session_state:
        st.session_state.chat_history_project = []

    # 显示历史聊天记录
    for msg in st.session_state.chat_history_project:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 聊天输入框
    if prompt := st.chat_input("向 AI 提问...", key="chat_input_project"):
        # 添加用户提问到历史记录
        st.session_state.chat_history_project.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 获取当前学生的代码内容
        current_student_code = st.session_state.get("code_input_area", "")

        # 构建 AI 上下文提示词
        context = (
            "你是一位耐心、友好的 Python 编程老师。学生正在进行‘猜数字’综合项目的练习，"
            "当前正在编写 if/elif/else 逻辑代码。"
            f"学生当前的代码是：```python\n{current_student_code}\n```
"
            "如果学生代码报错或逻辑不通，请给出引导性建议，尽量不要直接给出完整答案，鼓励学生自己思考。"
        )

        # 调用新版 openai 库
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
            reply = f"⚠️ AI 服务暂时不可用：{e}"

        # 添加 AI 回复到历史记录
        st.session_state.chat_history_project.append({"role": "assistant", "content": reply})
        # 重新运行页面以显示新的回复
        st.rerun()