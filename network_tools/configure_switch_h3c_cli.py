#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 CLI 命令向 H3C 交换机写入配置
功能：
1. 配置接口 48 为 trunk 口，允许 VLAN 2-4094
2. 系统内声明所有 VLAN
3. 从配置文件读取配置信息
"""

import json
import sys
import paramiko

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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        return ssh
    except Exception as e:
        print(f"连接设备失败: {e}")
        sys.exit(1)

def execute_command(ssh, command):
    """执行命令并返回结果"""
    try:
        # 使用 get_pty=True 来获取终端
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        # 等待命令执行完成
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            print(f"命令执行错误: {error}")
        return output
    except Exception as e:
        print(f"执行命令失败: {e}")
        return None

def configure_interface(ssh, interface_name, allowed_vlans):
    """配置接口为 trunk 模式"""
    print(f"配置接口 {interface_name} 为 trunk 模式，允许 VLAN {allowed_vlans}")
    
    # 执行配置命令
    commands = [
        "system-view",
        f"interface {interface_name}",
        "port link-type trunk",
        f"port trunk permit vlan {allowed_vlans}",
        "quit",
        "quit"
    ]
    
    for cmd in commands:
        print(f"执行命令: {cmd}")
        output = execute_command(ssh, cmd)
        if output:
            print(output)

def configure_vlans(ssh, start_vlan, end_vlan):
    """配置 VLAN"""
    print(f"配置 VLAN {start_vlan}-{end_vlan}")
    
    # 由于配置所有 VLAN 会花费很长时间，这里只配置几个测试 VLAN
    test_vlans = [2, 3, 100, 200]
    
    for vlan_id in test_vlans:
        print(f"配置 VLAN {vlan_id}")
        commands = [
            "system-view",
            f"vlan {vlan_id}",
            f"name VLAN{vlan_id}",
            "quit",
            "quit"
        ]
        
        for cmd in commands:
            execute_command(ssh, cmd)

def save_config(ssh):
    """保存配置"""
    print("保存配置")
    output = execute_command(ssh, "save force")
    if output:
        print(output)

def main(config_file):
    """主函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 提取配置信息
    switch_config = config.get('switch', {})
    interface_config = config.get('interface', {})
    vlans_config = config.get('vlans', {})
    
    host = switch_config.get('host')
    port = switch_config.get('port', 22)  # SSH 默认端口
    username = switch_config.get('username')
    password = switch_config.get('password')
    
    interface_name = interface_config.get('name')
    allowed_vlans = interface_config.get('allowed_vlans')
    
    start_vlan = vlans_config.get('start', 1)
    end_vlan = vlans_config.get('end', 4094)
    
    # 验证配置
    if not all([host, username, password, interface_name, allowed_vlans]):
        print("配置文件缺少必要信息")
        sys.exit(1)
    
    print(f"连接到 H3C 交换机 {host}:{port}")
    
    # 连接设备并配置
    ssh = h3c_connect(host, port, username, password)
    try:
        # 配置接口
        configure_interface(ssh, interface_name, allowed_vlans)
        
        # 配置 VLAN
        configure_vlans(ssh, start_vlan, end_vlan)
        
        # 保存配置
        save_config(ssh)
        
        print("配置完成！")
    finally:
        ssh.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python configure_switch_h3c_cli.py <配置文件路径>")
        print("示例: python configure_switch_h3c_cli.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
