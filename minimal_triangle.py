#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化三角形判断程序
"""

import tkinter as tk

print("启动最小化三角形程序...")

class MinimalTriangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("三角形判断")
        self.root.geometry("400x300")
        
        # 输入框
        self.entry1 = tk.Entry(root, width=10)
        self.entry1.pack(pady=5)
        
        self.entry2 = tk.Entry(root, width=10)
        self.entry2.pack(pady=5)
        
        self.entry3 = tk.Entry(root, width=10)
        self.entry3.pack(pady=5)
        
        # 结果标签
        self.result = tk.Label(root, text="请输入三个数字", font=("微软雅黑", 14))
        self.result.pack(pady=20)
        
        # 按钮
        button = tk.Button(root, text="判断", command=self.judge)
        button.pack(pady=10)
    
    def judge(self):
        print("按钮点击事件触发")
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            c = float(self.entry3.get())
            print(f"输入: {a}, {b}, {c}")
            
            # 简单判断
            if a + b > c and a + c > b and b + c > a:
                self.result.config(text="可以组成三角形")
            else:
                self.result.config(text="不能组成三角形")
            print("判断完成")
        except Exception as e:
            self.result.config(text=f"错误: {e}")
            print(f"错误: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinimalTriangleApp(root)
    print("程序启动完成")
    root.mainloop()
