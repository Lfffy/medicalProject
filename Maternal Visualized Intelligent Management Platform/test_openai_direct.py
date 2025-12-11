import openai
import os
import sys

# 设置系统编码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 设置OpenAI API密钥
openai.api_key = os.environ.get('OPENAI_API_KEY', '您的OpenAI API密钥')  # 从环境变量获取或直接设置

def test_openai_api():
    try:
        # 调用OpenAI API生成响应
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "您是一位专业的医疗健康助手，用自然、友好的语言回答用户的问题。请避免使用过于专业的术语，确保回答通俗易懂。"
                },
                {
                    "role": "user",
                    "content": "我今年35岁，血压140/90，BMI 28，请问我的子痫前期风险高吗？"
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        # 获取AI生成的响应
        ai_response = response.choices[0].message.content.strip()
        print(f"OpenAI API响应成功:")
        print(f"{ai_response}")
        return True
    except Exception as e:
        print(f"OpenAI API调用失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("正在测试OpenAI API调用...")
    success = test_openai_api()
    if success:
        print("测试成功！OpenAI API可以正常调用。")
    else:
        print("测试失败！请检查API密钥和网络连接。")
