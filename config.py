import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
MODEL = os.environ.get("MODEL", "Qwen/Qwen2.5-7B-Instruct")
