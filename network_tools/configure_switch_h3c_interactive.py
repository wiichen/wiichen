#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过交互式 CLI 命令向 H3C 交换机写入配置
"""

import json
import sys
import paramiko
import time

def load_config(config_file):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        sys.exit(1)

def h3c_connect(host, port, username, password):
    """连接到 H3C 设备"""
    try:
        # 创建 SSH 客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 配置 SSH 选项
        ssh_config = paramiko.SSHConfig()
        
        # 连接到设备
        print(f"正在连接到 {host}:{port}...")
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=15,
            allow_agent=False,
            look_for_keys=False,
            compress=True
        )
        print("连接成功！")
        return ssh
    except paramiko.AuthenticationException as e:
        print(f"认证失败: {e}")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"SSH 连接失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"连接设备失败: {e}")
        sys.exit(1)

def execute_commands(ssh, commands):
    """执行命令并显示输出"""
    try:
        # 打开交互式 shell
        channel = ssh.invoke_shell()
        channel.settimeout(30)
        
        # 等待提示符
        time.sleep(1)
        output = b''
        while channel.recv_ready():
            output += channel.recv(4096)
        print(output.decode('utf-8', errors='ignore'))
        
        # 执行命令
        for command in commands:
            print(f"\n[执行命令]: {command}")
            channel.send(command + '\n')
            
            # 等待命令执行完成
            time.sleep(2)
            
            # 读取输出
            output = b''
            while channel.recv_ready():
                output += channel.recv(4096)
                time.sleep(0.1)
            
            # 显示输出
            output_str = output.decode('utf-8', errors='ignore')
            print(output_str)
            
            # 检查是否有错误
            if 'Error:' in output_str or '% Error' in output_str:
                print("命令执行出错！")
                channel.close()
                return False
        
        # 关闭通道
        channel.close()
        return True
    except Exception as e:
        print(f"执行命令失败: {e}")
        return False

def main(config_file):
    """主函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 提取配置信息
    switch_config = config.get('switch', {})
    interface_config = config.get('interface', {})
    
    host = switch_config.get('host')
    port = switch_config.get('port', 22)
    username = switch_config.get('username')
    password = switch_config.get('password')
    
    interface_name = interface_config.get('name')
    allowed_vlans = interface_config.get('allowed_vlans')
    
    # 验证配置
    if not all([host, username, password, interface_name, allowed_vlans]):
        print("配置文件缺少必要信息")
        sys.exit(1)
    
    print(f"配置 H3C 交换机: {host}")
    
    # 连接设备
    ssh = h3c_connect(host, port, username, password)
    
    try:
        # 配置命令序列
        commands = [
            # 配置接口为 trunk 模式
            "system-view",
            f"interface {interface_name}",
            "port link-type trunk",
            f"port trunk permit vlan {allowed_vlans}",
            "quit",
            
            # 配置 VLAN
            "vlan 2",
            "name VLAN2",
            "quit",
            "vlan 3",
            "name VLAN3",
            "quit",
            "vlan 100",
            "name VLAN100",
            "quit",
            
            # 保存配置
            "save force",
            "y",  # 确认保存
            
            # 退出
            "quit"
        ]
        
        # 执行命令
        success = execute_commands(ssh, commands)
        
        if success:
            print("\n✅ 配置完成！")
        else:
            print("\n❌ 配置失败！")
            
    finally:
        # 关闭连接
        ssh.close()
        print("连接已关闭")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python configure_switch_h3c_interactive.py <配置文件路径>")
        print("示例: python configure_switch_h3c_interactive.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
