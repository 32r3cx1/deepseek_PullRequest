import os
import requests
import glob

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://platform.deepseek.com/api_keys"  # 假设的 API 地址
API_KEY = os.getenv("DEEPSEEK_APIKEY")  # 从 GitHub Secrets 获取

def analyze_code(file_path):
    """发送代码到 DeepSeek API 进行分析"""
    with open(file_path, 'r') as f:
        code = f.read()

    prompt = f"""
    请审查以下代码并指出潜在问题：
    - 循环嵌套过深（>3层）
    - 可能的性能瓶颈（如未优化的循环）
    - 代码风格问题（PEP 8 违规）
    - 潜在 Bug（如未处理的异常、逻辑错误）
    - 安全风险（如 SQL 注入、硬编码密码）

    请用 Markdown 格式返回结果，包含具体的行号和建议。

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
        "model": "deepseek-coder",  # 假设 DeepSeek 有代码专用模型
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3  # 降低随机性，使反馈更稳定
    }

    response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def main():
    """遍历所有修改的 Python 文件并分析"""
    changed_files = glob.glob("**/*.py", recursive=True)  # 获取所有 .py 文件

    all_comments = []
    for file in changed_files:
        print(f"正在分析: {file}")
        review = analyze_code(file)
        all_comments.append(f"## 📄 {file}\n\n{review}")

    # 保存结果到文件，供后续 GitHub Action 读取
    with open("review_result.md", "w") as f:
        f.write("\n\n".join(all_comments))

if __name__ == "__main__":
    main()
