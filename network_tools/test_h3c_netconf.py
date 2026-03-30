#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 H3C 交换机的 NETCONF 实现
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
        return manager.connect(
            host=host,
            port=port,
            username=user,
            password=password,
            hostkey_verify=False,
            device_params={'name': "h3c"},
            allow_agent=False,
            look_for_keys=False
        )
    except Exception as e:
        print(f"连接设备失败: {e}")
        sys.exit(1)

def test_capabilities(m):
    """测试设备能力"""
    print("\n=== 设备能力 ===")
    capabilities = m.server_capabilities
    for cap in capabilities:
        print(f"- {cap}")

def test_get_config(m):
    """测试获取配置"""
    print("\n=== 测试获取配置 ===")
    try:
        # 获取接口配置
        filter_xml = '''
        <filter>
            <ifm xmlns="http://www.h3c.com/netconf/config:1.0">
                <interfaces>
                    <interface>
                        <name>GigabitEthernet0/0/48</name>
                    </interface>
                </interfaces>
            </ifm>
        </filter>
        '''
        
        response = m.get_config(source='running', filter=filter_xml)
        print("获取接口配置成功:")
        print(response.xml)
    except Exception as e:
        print(f"获取配置失败: {e}")

def test_edit_interface(m):
    """测试配置接口"""
    print("\n=== 测试配置接口 ===")
    
    # 尝试不同的 XML 结构
    config_xmls = [
        # 结构 1: 简化版
        '''
        <config>
            <ifm xmlns="http://www.h3c.com/netconf/config:1.0">
                <interfaces>
                    <interface>
                        <name>GigabitEthernet0/0/48</name>
                        <ethernet>
                            <switchport>
                                <mode>trunk</mode>
                            </switchport>
                        </ethernet>
                    </interface>
                </interfaces>
            </ifm>
        </config>
        ''',
        # 结构 2: 更简化的版本
        '''
        <config>
            <interface xmlns="http://www.h3c.com/netconf/config:1.0">
                <name>GigabitEthernet0/0/48</name>
                <switchport>
                    <mode>trunk</mode>
                    <trunk>
                        <allowed-vlans>2-4094</allowed-vlans>
                    </trunk>
                </switchport>
            </interface>
        </config>
        ''',
        # 结构 3: 使用标准 NETCONF 格式
        '''
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>GigabitEthernet0/0/48</name>
                    <type xmlns:iana="urn:ietf:params:xml:ns:iana-if-type">iana:ethernetCsmacd</type>
                </interface>
            </interfaces>
        </config>
        '''
    ]
    
    for i, config_xml in enumerate(config_xmls):
        print(f"\n尝试配置结构 {i+1}:")
        try:
            response = m.edit_config(target='running', config=config_xml)
            print(f"配置成功: {response}")
            break
        except Exception as e:
            print(f"配置失败: {e}")

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
    
    print(f"连接到 H3C 交换机 {host}:{port}")
    
    # 连接设备
    with h3c_connect(host, port, username, password) as m:
        print(f"成功连接到设备，会话 ID: {m._session.id}")
        
        # 测试设备能力
        test_capabilities(m)
        
        # 测试获取配置
        test_get_config(m)
        
        # 测试配置接口
        test_edit_interface(m)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python test_h3c_netconf.py <配置文件路径>")
        print("示例: python test_h3c_netconf.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
