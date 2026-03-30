#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断 H3C 交换机连接问题
"""

import json
import sys
import socket
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

def test_network_connection(host, port):
    """测试网络连接"""
    print(f"\n=== 测试网络连接到 {host}:{port} ===")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print("✓ 网络连接成功！")
            return True
        else:
            print(f"✗ 网络连接失败，错误码: {result}")
            return False
    except Exception as e:
        print(f"✗ 网络连接测试失败: {e}")
        return False
    finally:
        sock.close()

def test_ssh_connection(host, port, username, password):
    """测试 SSH 连接"""
    print(f"\n=== 测试 SSH 连接到 {host}:{port} ===")
    print(f"用户名: {username}")
    print(f"密码: {'*' * len(password)}")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 尝试连接
        print("尝试连接...")
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        
        print("✓ SSH 连接成功！")
        
        # 尝试执行简单命令
        print("\n尝试执行命令...")
        stdin, stdout, stderr = ssh.exec_command("display version")
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print("命令执行成功，输出:")
            print(output[:500] + "..." if len(output) > 500 else output)
        if error:
            print("命令执行错误:")
            print(error)
        
        ssh.close()
        return True
        
    except paramiko.AuthenticationException as e:
        print(f"✗ 认证失败: {e}")
        return False
    except paramiko.SSHException as e:
        print(f"✗ SSH 连接失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False

def main(config_file):
    """主函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 提取配置信息
    switch_config = config.get('switch', {})
    
    host = switch_config.get('host')
    port = switch_config.get('port', 22)
    username = switch_config.get('username')
    password = switch_config.get('password')
    
    # 验证配置
    if not all([host, username, password]):
        print("配置文件缺少必要信息")
        sys.exit(1)
    
    print(f"诊断连接到 H3C 交换机: {host}")
    
    # 测试网络连接
    network_ok = test_network_connection(host, port)
    
    if network_ok:
        # 测试 SSH 连接
        test_ssh_connection(host, port, username, password)
    else:
        print("\n网络连接失败，无法继续测试 SSH 连接")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python diagnose_connection.py <配置文件路径>")
        print("示例: python diagnose_connection.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
