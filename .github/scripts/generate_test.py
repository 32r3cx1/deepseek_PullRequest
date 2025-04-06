import argparse
import base64

TEST_CASES = {
    "basic": """
def basic_test():
    # 基础测试用例
    x = 1
    return x
    """,
    "advance": """
def advance_test():
    # 高级测试用例
    for i in range(10):
        for j in range(10):
            print(i*j)
    """
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=TEST_CASES.keys(), default="basic")
    parser.add_argument("--code", help="Base64编码的自定义代码")
    parser.add_argument("--output", default="test_case.py")
    args = parser.parse_args()

    code = TEST_CASES[args.mode]
    if args.code:
        code = base64.b64decode(args.code.encode()).decode()

    with open(args.output, 'w') as f:
        f.write(code)

if __name__ == "__main__":
    main()
