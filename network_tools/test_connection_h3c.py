#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试连接到 H3C 交换机
"""

import json
import sys
from ncclient import manager

def load_config(config_file):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        sys.exit(1)

def h3c_connect(host, port, user, password):
    """连接到 H3C 设备"""
    try:
        print(f"尝试连接到 {host}:{port}...")
        return manager.connect(
            host=host,
            port=port,
            username=user,
            password=password,
            hostkey_verify=False,
            device_params={'name': "h3c"},
            allow_agent=False,
            look_for_keys=False,
            timeout=10
        )
    except Exception as e:
        print(f"连接设备失败: {e}")
        return None

def main(config_file):
    """主函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 提取配置信息
    switch_config = config.get('switch', {})
    
    host = switch_config.get('host')
    port = switch_config.get('port', 830)
    username = switch_config.get('username')
    password = switch_config.get('password')
    
    # 验证配置
    if not all([host, username, password]):
        print("配置文件缺少必要信息")
        sys.exit(1)
    
    print(f"测试连接到 H3C 交换机 {host}:{port}")
    
    # 连接设备
    m = h3c_connect(host, port, username, password)
    if m:
        print(f"成功连接到设备，会话 ID: {m._session.id}")
        
        # 尝试获取设备信息
        try:
            # 获取设备能力
            capabilities = m.server_capabilities
            print("设备能力:")
            for cap in list(capabilities)[:5]:  # 只显示前5个能力
                print(f"  - {cap}")
            
            # 关闭连接
            m.close()
            print("连接已关闭")
        except Exception as e:
            print(f"获取设备信息失败: {e}")
            m.close()
    else:
        print("连接失败，请检查网络连接和设备配置")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python test_connection_h3c.py <配置文件路径>")
        print("示例: python test_connection_h3c.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
