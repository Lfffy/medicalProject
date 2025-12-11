import os
import sys
from openai import OpenAI

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 初始化火山方舟OpenAI兼容客户端
client = OpenAI(
    # 火山方舟API地址
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 使用API密钥
    api_key="ceadb27c-39e4-4527-924d-a8bb5e81758e",
)

print("正在测试火山方舟大模型API调用...")

try:
    # 测试简单的对话
    completion = client.chat.completions.create(
        model="ep-20250514110428-r589j",
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": "你好，我是一位孕妇，今年35岁，血压140/90，BMI 28，请问我的子痫前期风险高吗？"},
        ],
    )
    print("API调用成功!")
    print(f"响应内容: {completion.choices[0].message.content}")
except Exception as e:
    print(f"API调用失败: {e}")
    import traceback
    traceback.print_exc()
