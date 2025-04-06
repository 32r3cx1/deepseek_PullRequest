import os
import argparse
from openai import OpenAI

def analyze_code(filepath):
    """DeepSeek API 审查核心逻辑"""
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_APIKEY"),
        base_url="https://api.deepseek.com"
    )
    
    with open(filepath, 'r') as f:
        code = f.read()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个专业的代码审查助手，用Markdown格式返回问题报告"},
            {"role": "user", "content": f"审查以下代码：\n```python\n{code}\n```"}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--output", default="review.md", help="输出文件路径")
    args = parser.parse_args()

    result = analyze_code(args.input)
    with open(args.output, 'w') as f:
        f.write(f"# DeepSeek 代码审查报告\n\n{result}")
