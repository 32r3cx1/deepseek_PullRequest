# DeepSeek 云端调试指南

## 快速开始
1. 在仓库设置中添加 `DEEPSEEK_APIKEY` Secrets
2. 进入 Actions → 选择工作流 → Run workflow
3. 选择测试模式或输入自定义代码（base64编码）

## 自定义测试代码
```bash
echo "你的代码" | base64
# 将输出结果填入custom_code参数
```
