#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三角形类型判断程序 - 主入口
提供命令行和图形界面两种运行模式
"""

import sys
import os

# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'


def print_menu():
    """
    打印主菜单
    """
    print("\n" + "=" * 50)
    print("       三角形类型判断程序")
    print("=" * 50)
    print("1. 命令行版本")
    print("2. 图形界面版本")
    print("3. 运行测试")
    print("0. 退出")
    print("=" * 50)


def run_console_version():
    """
    运行命令行版本
    """
    print("\n启动命令行版本...")
    import triangle
    triangle.main()


def run_gui_version():
    """
    运行图形界面版本
    """
    print("\n启动图形界面版本...")
    try:
        import triangle_gui
        triangle_gui.main()
    except ImportError as e:
        print(f"错误：无法启动图形界面 - {e}")
        print("请确保已安装 tkinter 库")


def run_tests():
    """
    运行测试
    """
    print("\n运行测试...")
    import test_triangle
    test_triangle.main()


def main():
    """
    主函数
    """
    while True:
        print_menu()
        choice = input("请选择运行模式 (0-3): ").strip()
        
        if choice == "1":
            run_console_version()
        elif choice == "2":
            run_gui_version()
        elif choice == "3":
            run_tests()
        elif choice == "0":
            print("\n感谢使用，再见！")
            break
        else:
            print("\n无效的选择，请重新输入！")


if __name__ == "__main__":
    main()
