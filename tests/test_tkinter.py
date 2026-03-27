#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试tkinter是否能正常工作
"""

import tkinter as tk
from tkinter import messagebox

print("测试tkinter...")

# 测试1: 基本窗口
print("测试1: 创建基本窗口")
root = tk.Tk()
root.title("测试窗口")
root.geometry("300x200")

# 测试2: 添加标签
print("测试2: 添加标签")
label = tk.Label(root, text="Hello tkinter!")
label.pack(pady=20)

# 测试3: 添加按钮
print("测试3: 添加按钮")
def button_click():
    print("按钮被点击了！")
    label.config(text="按钮被点击了！")

button = tk.Button(root, text="点击我", command=button_click)
button.pack(pady=10)

print("测试完成，启动主循环...")

# 启动主循环
root.mainloop()

print("主循环结束")
