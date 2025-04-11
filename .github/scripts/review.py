import os
import sys
import requests
from github import Github

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def analyze_file(file_path, api_key):
    """使用DeepSeek API分析单个文件"""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except Exception as e:
        return [f"Error reading {file_path}: {str(e)}"]

    prompt = f"""请严格按以下格式分析代码质量问题：
文件路径:行号: 问题级别: 问题描述

示例：
src/app.py:15: 警告: 循环嵌套过深（3层）可能影响性能
tests/unit.py:3: 建议: 缺少异常处理逻辑

需要分析的代码：
{code}

请只返回检测到的问题，不要其他内容。每个问题单独一行："""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return [
            line.strip()
            for line in response.json()["choices"][0]["message"]["content"].split("\n")
            if ":" in line and file_path in line
        ]
    except Exception as e:
        return [f"API Error: {str(e)}"]

def main():
    changed_files = sys.argv[1].split()
    issues = []
    
    for file_path in changed_files:
        if os.path.exists(file_path) and file_path.endswith(('.py', '.js', '.java')):
            issues += analyze_file(file_path, os.getenv("DEEPSEEK_API_KEY"))
    
    if issues:
        comment = "🔍 DeepSeek 代码审查报告\n\n" + "\n".join(
            [f"⚠️ `{issue}`" for issue in issues]
        )
        
        github = Github(os.getenv("GITHUB_TOKEN"))
        repo = github.get_repo(os.getenv("GITHUB_REPOSITORY"))
        pr_number = int(os.getenv("GITHUB_REF").split("/")[-2])
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)

if __name__ == "__main__":
    main()
