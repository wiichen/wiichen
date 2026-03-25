#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试按钮点击功能
"""

import tkinter as tk

print("启动按钮测试程序...")

root = tk.Tk()
root.title("按钮测试")
root.geometry("300x200")

# 结果标签
result_label = tk.Label(root, text="点击按钮", font=("微软雅黑", 14))
result_label.pack(pady=20)

# 按钮点击函数
def on_click():
    print("按钮被点击了！")
    result_label.config(text="按钮被点击了！")

# 按钮
button = tk.Button(
    root,
    text="点击我",
    font=("微软雅黑", 12),
    command=on_click
)
button.pack(pady=10)

print("程序启动完成")
root.mainloop()
