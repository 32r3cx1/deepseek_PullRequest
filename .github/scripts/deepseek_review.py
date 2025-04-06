import os
import requests
import glob
from pathlib import Path

# DeepSeek API 配置（需确认实际API地址）
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/generate‌"  # 假设地址
API_KEY = os.getenv("DEEPSEEK_APIKEY")  # 确保与GitHub Secrets一致

def analyze_code(file_path):
    """发送代码到 DeepSeek API 进行分析"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        prompt = f"""
        请审查以下代码并指出潜在问题：
        - 循环嵌套过深（>3层）
        - 可能的性能瓶颈
        - 代码风格问题（PEP 8）
        - 潜在 Bug 或安全风险

        请用 Markdown 格式返回结果，包含具体行号和建议。

        代码：
        ```python
        {code}
        ```
        """

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-coder",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }

        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()  # 检查HTTP状态码

        response_data = response.json()
        if "choices" not in response_data:
            return "API返回格式异常，缺少choices字段"

        return response_data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ 分析失败: {str(e)}"

def main():
    """遍历所有.py文件并分析"""
    changed_files = glob.glob("**/*.py", recursive=True)
    all_comments = []

    for file in changed_files:
        print(f"正在分析: {file}")
        review = analyze_code(file)
        all_comments.append(f"## 📄 {file}\n\n{review}")

    # 确保目录存在
    Path(".github/scripts").mkdir(parents=True, exist_ok=True)
    
    with open("review_result.md", "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_comments))

if __name__ == "__main__":
    main()
