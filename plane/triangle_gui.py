#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全新的三角形判断图形界面程序
"""

import tkinter as tk
import datetime

def main():
    print("启动全新三角形程序...")
    # 创建主窗口
    root = tk.Tk()
    root.title("三角形类型判断程序")
    root.geometry("500x400")
    root.config(bg="#4a6572")
    
    # 标题
    label_title = tk.Label(
        root,
        text="三角形类型判断程序",
        font=("微软雅黑", 20, "bold"),
        bg="#4a6572",
        fg="#ffffff"
    )
    label_title.pack(pady=20)
    
    # 输入框
    entries = []
    for i in range(3):
        frame = tk.Frame(root, bg="#4a6572")
        frame.pack(pady=10)
        
        label = tk.Label(
            frame,
            text=f"第 {i+1} 条边：",
            font=("微软雅黑", 12),
            bg="#4a6572",
            fg="#ffffff"
        )
        label.pack(side=tk.LEFT, padx=10)
        
        entry = tk.Entry(
            frame,
            font=("微软雅黑", 12),
            width=15
        )
        entry.pack(side=tk.LEFT)
        entries.append(entry)
    
    # 结果标签
    result_label = tk.Label(
        root,
        text="请输入三个数字",
        font=("微软雅黑", 16, "bold"),
        bg="#4a6572",
        fg="#ff0000"
    )
    result_label.pack(pady=20, fill=tk.X)
    
    # 时间戳标签
    timestamp_label = tk.Label(
        root,
        text="",
        font=("微软雅黑", 10),
        bg="#344955",
        fg="#ffffff",
        padx=10,
        pady=5
    )
    timestamp_label.place(x=10, y=370)
    
    # 更新时间戳
    def update_timestamp():
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp_label.config(text=f"时间：{time}")
        root.after(1000, update_timestamp)
    
    # 三角形判断函数
    def judge_triangle():
        print("按钮被点击！")
        try:
            # 获取输入
            a = float(entries[0].get().strip())
            b = float(entries[1].get().strip())
            c = float(entries[2].get().strip())
            
            print(f"输入值: {a}, {b}, {c}")
            
            # 检查是否为正数
            if a <= 0 or b <= 0 or c <= 0:
                result_label.config(text="错误：输入必须为正数！", fg="#ff0000")
                return
            
            # 判断三角形类型
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
            result_label.config(text=f"结果：{result}", fg="#ff0000")
            
        except ValueError:
            result_label.config(text="错误：请输入有效的数字！", fg="#ff0000")
        except Exception as e:
            result_label.config(text=f"错误：{e}", fg="#ff0000")
    
    # 清除函数
    def clear_entries():
        for entry in entries:
            entry.delete(0, tk.END)
        result_label.config(text="请输入三个数字", fg="#ff0000")
    
    # 按钮
    button_frame = tk.Frame(root, bg="#4a6572")
    button_frame.pack(pady=20)
    
    judge_button = tk.Button(
        button_frame,
        text="判断三角形",
        font=("微软雅黑", 12, "bold"),
        bg="#344955",
        fg="#ffffff",
        command=judge_triangle
    )
    judge_button.pack(side=tk.LEFT, padx=10)
    
    clear_button = tk.Button(
        button_frame,
        text="清除",
        font=("微软雅黑", 12),
        bg="#344955",
        fg="#ffffff",
        command=clear_entries
    )
    clear_button.pack(side=tk.LEFT, padx=10)
    
    # 启动时间戳更新
    update_timestamp()
    
    print("程序启动完成")
    root.mainloop()

if __name__ == "__main__":
    main()
