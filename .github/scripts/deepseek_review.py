import os
from openai import OpenAI
import glob

def analyze_code(file_path):
    """使用 DeepSeek 官方 API 审查代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_APIKEY"),
            base_url="https://api.deepseek.com"
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的Python代码审查助手，需严格检查：\n"
                               "1. 代码缺陷（用❌标记）\n"
                               "2. 优化建议（用💡标记）\n"
                               "3. 安全风险（用🔒标记）\n"
                               "要求：按行号给出Markdown格式报告"
                },
                {
                    "role": "user",
                    "content": f"请审查以下代码：\n```python\n{code}\n```"
                }
            ],
            temperature=0.2,
            max_tokens=2000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ 审查失败: {str(e)}"

def main():
    """主执行函数"""
    all_comments = ["## DeepSeek-V3 代码审查报告"]
    
    # 获取所有.py文件
    for file in glob.glob("**/*.py", recursive=True):
        print(f"正在审查: {file}")
        review = analyze_code(file)
        all_comments.append(f"### {file}\n{review}\n")

    # 始终生成报告文件
    with open("review_result.md", "w", encoding="utf-8") as f:
        f.write("\n".join(all_comments)

if __name__ == "__main__":
    main()
