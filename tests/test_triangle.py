#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试三角形类型判断程序
自动提供不同的测试用例
"""

import subprocess
import sys
import os

# 设置环境变量，强制使用 UTF-8 编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 测试用例
test_cases = [
    # (输入值, 预期结果)
    (["3", "3", "3"], "等边三角形"),          # 等边三角形
    (["3", "3", "4"], "等腰三角形"),          # 等腰三角形
    (["3", "4", "5"], "普通直角三角形"),      # 直角三角形（3² + 4² = 5²）
    (["4", "5", "6"], "普通锐角三角形"),      # 锐角三角形（4² + 5² = 41 > 6² = 36）
    (["3", "4", "6"], "普通钝角三角形"),      # 钝角三角形（3² + 4² = 25 < 6² = 36）
    (["1", "1", "3"], "不能组成三角形"),      # 不能组成三角形
    (["0", "1", "1"], "不能组成三角形"),      # 非正数输入
    (["5", "12", "13"], "普通直角三角形"),    # 直角三角形（5² + 12² = 13²）
    (["2", "3", "4"], "普通钝角三角形"),      # 钝角三角形（2² + 3² = 13 < 4² = 16）
    (["6", "7", "8"], "普通锐角三角形"),      # 锐角三角形（6² + 7² = 85 > 8² = 64）
]

def run_test(input_values):
    """
    运行测试用例
    """
    # 构建输入字符串
    input_str = "\n".join(input_values) + "\n"
    
    # 运行三角形判断程序
    # 设置编码为 utf-8 以避免 Windows 默认 gbk 编码导致的错误
    result = subprocess.run(
        [sys.executable, "triangle.py"],
        input=input_str,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'  # 使用 replace 来处理无法解码的字符
    )
    
    return result.stdout

def main():
    """
    运行所有测试用例
    """
    print("===== 测试三角形类型判断程序 =====")
    
    for i, (input_values, expected) in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: 输入 {input_values}")
        print(f"预期结果: {expected}")
        
        try:
            output = run_test(input_values)
            print(f"程序输出:\n{output}")
            
            # 检查结果是否包含预期字符串
            if output and expected in output:
                print("✓ 测试通过")
            else:
                print("✗ 测试失败")
        except Exception as e:
            print(f"✗ 测试出错: {e}")
    
    print("\n===== 测试完成 =====")

if __name__ == "__main__":
    main()
