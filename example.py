def calculate_stats(data):
    # 问题1：嵌套循环过深（4层）
    results = []
    for i in range(100):
        for j in range(100):
            for k in range(100):
                for l in range(100):  # DeepSeek 应检测到并警告
                    results.append(i + j + k + l)
    
    # 问题2：未处理文件异常
    file = open("missing_file.txt", "r")  # 未处理 FileNotFoundError
    content = file.read()
    
    # 问题3：变量命名不规范
    BadNamedVar = 123  # 应改为 snake_case（如 bad_named_var）
    
    return results