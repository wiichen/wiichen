#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三角形类型判断程序
功能：
1. 输入三个数字作为三角形的三边长度
2. 处理输入异常（如非数字输入）
3. 判断能否组成三角形，以及三角形的类型（等边、等腰、普通）
4. 显示操作时间戳
5. 使用标准库logging记录日志
"""

import logging
import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='triangle.log',  # 日志文件
    filemode='a'  # 追加模式
)

# 定义日志记录器
logger = logging.getLogger(__name__)

def get_timestamp():
    """
    获取当前时间戳
    返回格式：YYYY-MM-DD HH:MM:SS
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_user_input():
    """
    获取用户输入的三个数字
    处理输入异常，确保输入为有效的数字
    """
    while True:
        try:
            # 提示用户输入三个数字
            a = float(input("请输入第一个数字："))
            b = float(input("请输入第二个数字："))
            c = float(input("请输入第三个数字："))
            
            # 检查输入是否为正数
            if a <= 0 or b <= 0 or c <= 0:
                print("错误：输入必须为正数！")
                logger.warning(f"输入非正数: a={a}, b={b}, c={c}")
                continue
            
            return a, b, c
        except ValueError as e:
            # 捕获非数字输入异常
            print(f"错误：输入必须为数字！{e}")
            logger.error(f"输入非数字: {e}")
            continue

def judge_triangle(a, b, c):
    """
    判断三角形类型
    参数：
        a, b, c: 三角形的三边长度
    返回：
        str: 三角形类型或不能组成三角形的提示
    """
    # 排序三边，方便后续判断
    sides = sorted([a, b, c])
    a, b, c = sides[0], sides[1], sides[2]
    
    # 判断是否能组成三角形（任意两边之和大于第三边）
    if a + b <= c:
        return "不能组成三角形"
    
    # 判断三角形类型
    if a == b == c:
        return "等边三角形"
    elif a == b or b == c:
        return "等腰三角形"
    else:
        # 普通三角形进一步细分为锐角、直角、钝角三角形
        # 使用勾股定理判断：c为最长边
        # a² + b² = c² 为直角三角形
        # a² + b² > c² 为锐角三角形
        # a² + b² < c² 为钝角三角形
        a2, b2, c2 = a**2, b**2, c**2
        
        if abs(a2 + b2 - c2) < 1e-9:  # 考虑浮点数精度问题
            return "普通直角三角形"
        elif a2 + b2 > c2:
            return "普通锐角三角形"
        else:
            return "普通钝角三角形"
        

def main():
    """
    主函数
    1. 获取用户输入
    2. 判断三角形类型
    3. 显示时间戳和结果
    4. 记录日志
    """
    print("===== 三角形类型判断程序 =====")
    
    # 获取当前时间戳
    timestamp = get_timestamp()
    print(f"操作时间：{timestamp}")
    
    # 获取用户输入
    a, b, c = get_user_input()
    
    # 判断三角形类型
    result = judge_triangle(a, b, c)
    
    # 显示结果
    print(f"\n结果：{result}")
    print(f"三边长度：{a}, {b}, {c}")
    
    # 记录日志
    logger.info(f"时间: {timestamp}, 输入: {a}, {b}, {c}, 结果: {result}")
    
    print("\n===== 程序结束 =====")

if __name__ == "__main__":
    main()
