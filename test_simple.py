#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试程序，测试按钮点击和标签更新
"""

import tkinter as tk

print("启动简化测试程序...")

root = tk.Tk()
root.title("测试程序")
root.geometry("400x300")
root.config(bg="#4a6572")

# 输入框
entry1 = tk.Entry(root, width=10, font=("微软雅黑", 12))
entry1.pack(pady=10)

entry2 = tk.Entry(root, width=10, font=("微软雅黑", 12))
entry2.pack(pady=10)

entry3 = tk.Entry(root, width=10, font=("微软雅黑", 12))
entry3.pack(pady=10)

# 结果标签
result_label = tk.Label(
    root,
    text="请输入三个数字",
    font=("微软雅黑", 16, "bold"),
    bg="#4a6572",
    fg="#ff0000"
)
result_label.pack(pady=20, fill=tk.X)

# 按钮点击函数
def on_click():
    print("按钮被点击")
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        c = float(entry3.get())
        print(f"输入值: {a}, {b}, {c}")
        
        # 简单的三角形判断
        if a + b <= c or a + c <= b or b + c <= a:
            result = "不能组成三角形"
        else:
            result = "可以组成三角形"
        
        print(f"结果: {result}")
        result_label.config(text=f"结果：{result}", fg="#ff0000")
        root.update()
        print("标签已更新")
    except Exception as e:
        print(f"错误: {e}")
        result_label.config(text=f"错误: {e}", fg="#ff0000")

# 按钮
button = tk.Button(
    root,
    text="判断",
    font=("微软雅黑", 12),
    bg="#344955",
    fg="#ffffff",
    command=on_click
)
button.pack(pady=10)

print("程序启动完成")
root.mainloop()
