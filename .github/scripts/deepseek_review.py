import os
import requests
import glob

# DeepSeek API 配置
BASE_URL = "https://api.deepseek.com"
API_ENDPOINT = "/v1/generate"
API_KEY = os.getenv("DEEPSEEK_APIKEY")  # 与Secrets完全一致

def analyze_code(file_path):
    """发送代码到 DeepSeek API 进行分析"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        prompt = f"""
        请严格审查以下Python代码：
        1. 代码质量问题（嵌套循环、复杂度过高）
        2. 潜在bug（边界条件、异常处理）
        3. PEP 8风格违规
        4. 安全风险
        
        要求：
        - 按严重程度分级（⚠️警告/❌错误）
        - 标明具体行号
        - 给出修改建议
        
        代码：
        ```python
        {code}
        ```
        """

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = {
            "model": "deepseek-coder",
            "prompt": prompt,  # 根据实际API文档调整字段
            "max_tokens": 2000,
            "temperature": 0.2
        }

        response = requests.post(
            f"{BASE_URL}{API_ENDPOINT}",
            json=data,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        response_data = response.json()
        
        # 根据实际API响应结构调整解析逻辑
        if "choices" in response_data:
            return response_data["choices"][0]["text"]
        elif "output" in response_data:
            return response_data["output"]
        else:
            return str(response_data)  # 调试用返回原始响应

    except Exception as e:
        return f"❌ 审查失败: {str(e)}\n响应内容: {response.text if 'response' in locals() else '无响应'}"

def main():
    """主执行函数"""
    changed_files = glob.glob("**/*.py", recursive=True)
    
    if not changed_files:
        print("未发现.py文件")
        with open("review_result.md", "w") as f:
            f.write("未发现需要审查的Python文件")
        return

    all_comments = ["## DeepSeek AI 代码审查报告"]
    
    for file in changed_files:
        print(f"正在审查: {file}")
        review = analyze_code(file)
        all_comments.append(f"### 文件: {file}\n\n{review}\n")

    with open("review_result.md", "w", encoding="utf-8") as f:
        f.write("\n".join(all_comments))

if __name__ == "__main__":
    main()
