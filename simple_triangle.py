#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版三角形判断程序
"""

import tkinter as tk
import datetime

print("启动简化版三角形程序...")

class SimpleTriangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("三角形判断")
        self.root.geometry("400x300")
        self.root.config(bg="#4a6572")
        
        # 标题
        title = tk.Label(
            root,
            text="三角形类型判断",
            font=("微软雅黑", 18, "bold"),
            bg="#4a6572",
            fg="#ffffff"
        )
        title.pack(pady=10)
        
        # 输入框
        self.entries = []
        for i in range(3):
            frame = tk.Frame(root, bg="#4a6572")
            frame.pack(pady=5)
            
            label = tk.Label(
                frame,
                text=f"边 {i+1}: ",
                font=("微软雅黑", 12),
                bg="#4a6572",
                fg="#ffffff"
            )
            label.pack(side=tk.LEFT, padx=10)
            
            entry = tk.Entry(
                frame,
                width=10,
                font=("微软雅黑", 12)
            )
            entry.pack(side=tk.LEFT)
            self.entries.append(entry)
        
        # 结果标签
        self.result_label = tk.Label(
            root,
            text="请输入三个数字",
            font=("微软雅黑", 16, "bold"),
            bg="#4a6572",
            fg="#ff0000"
        )
        self.result_label.pack(pady=20, fill=tk.X)
        
        # 按钮
        button = tk.Button(
            root,
            text="判断三角形",
            font=("微软雅黑", 12, "bold"),
            bg="#344955",
            fg="#ffffff",
            command=self.judge
        )
        button.pack(pady=10)
        
        # 时间戳
        self.timestamp_label = tk.Label(
            root,
            text="",
            font=("微软雅黑", 10),
            bg="#4a6572",
            fg="#ffffff"
        )
        self.timestamp_label.place(x=10, y=270)
        self.update_timestamp()
    
    def update_timestamp(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.timestamp_label.config(text=f"时间：{time}")
        self.root.after(1000, self.update_timestamp)
    
    def judge(self):
        print("按钮被点击")
        try:
            # 获取输入
            a = float(self.entries[0].get())
            b = float(self.entries[1].get())
            c = float(self.entries[2].get())
            
            print(f"输入: {a}, {b}, {c}")
            
            # 判断三角形
            sides = sorted([a, b, c])
            a, b, c = sides[0], sides[1], sides[2]
            
            if a + b <= c:
                result = "不能组成三角形"
            elif a == b == c:
                result = "等边三角形"
            elif a == b or b == c:
                result = "等腰三角形"
            else:
                a2, b2, c2 = a**2, b**2, c**2
                if abs(a2 + b2 - c2) < 1e-9:
                    result = "普通直角三角形"
                elif a2 + b2 > c2:
                    result = "普通锐角三角形"
                else:
                    result = "普通钝角三角形"
            
            print(f"结果: {result}")
            self.result_label.config(text=f"结果：{result}")
            
        except Exception as e:
            print(f"错误: {e}")
            self.result_label.config(text=f"错误：{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTriangleApp(root)
    print("程序启动完成")
    root.mainloop()
