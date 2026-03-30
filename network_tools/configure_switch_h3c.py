#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 NETCONF 向 H3C 交换机写入配置
功能：
1. 配置接口 48 为 trunk 口，允许 VLAN 2-4094
2. 系统内声明所有 VLAN
3. 从配置文件读取配置信息
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

def configure_interface(m, interface_name, allowed_vlans):
    """配置接口为 trunk 模式"""
    print(f"配置接口 {interface_name} 为 trunk 模式，允许 VLAN {allowed_vlans}")
    
    # H3C NETCONF 配置 XML
    config_xml = f'''
    <config>
        <ifm xmlns="http://www.h3c.com/netconf/config:1.0">
            <interfaces>
                <interface>
                    <name>{interface_name}</name>
                    <type>ethernetCsmacd</type>
                    <enabled>true</enabled>
                    <mtu>1500</mtu>
                    <phy-attribute>
                        <duplex>auto</duplex>
                        <speed>auto</speed>
                    </phy-attribute>
                    <ethernet>
                        <switchport>
                            <mode>trunk</mode>
                            <trunk>
                                <allowed-vlans>{allowed_vlans}</allowed-vlans>
                            </trunk>
                        </switchport>
                    </ethernet>
                </interface>
            </interfaces>
        </ifm>
    </config>
    '''
    
    try:
        response = m.edit_config(target='running', config=config_xml)
        print(f"接口配置成功: {response}")
    except Exception as e:
        print(f"接口配置失败: {e}")

def configure_vlans(m, start_vlan, end_vlan):
    """配置 VLAN"""
    print(f"配置 VLAN {start_vlan}-{end_vlan}")
    
    # 为了避免一次性配置太多 VLAN 导致超时，分批次配置
    batch_size = 50
    current_vlan = start_vlan
    
    while current_vlan <= end_vlan:
        batch_end = min(current_vlan + batch_size - 1, end_vlan)
        print(f"配置 VLAN {current_vlan}-{batch_end}")
        
        # 构建 VLAN 配置 XML
        vlan_configs = []
        for vlan_id in range(current_vlan, batch_end + 1):
            vlan_configs.append(f'''
                <vlan>
                    <vlan-id>{vlan_id}</vlan-id>
                    <name>VLAN{vlan_id}</name>
                    <status>active</status>
                </vlan>
            ''')
        
        config_xml = f'''
        <config>
            <vlan xmlns="http://www.h3c.com/netconf/config:1.0">
                <vlans>
                    {''.join(vlan_configs)}
                </vlans>
            </vlan>
        </config>
        '''
        
        try:
            response = m.edit_config(target='running', config=config_xml)
            print(f"VLAN {current_vlan}-{batch_end} 配置成功")
        except Exception as e:
            print(f"VLAN {current_vlan}-{batch_end} 配置失败: {e}")
        
        current_vlan = batch_end + 1

def main(config_file):
    """主函数"""
    # 加载配置
    config = load_config(config_file)
    
    # 提取配置信息
    switch_config = config.get('switch', {})
    interface_config = config.get('interface', {})
    vlans_config = config.get('vlans', {})
    
    host = switch_config.get('host')
    port = switch_config.get('port', 830)
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
    with h3c_connect(host, port, username, password) as m:
        print(f"成功连接到设备，会话 ID: {m._session.id}")
        
        # 配置接口
        configure_interface(m, interface_name, allowed_vlans)
        
        # 配置 VLAN
        configure_vlans(m, start_vlan, end_vlan)
        
        # 提交配置
        try:
            m.commit()
            print("配置已提交")
        except Exception as e:
            print(f"提交配置失败: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python configure_switch_h3c.py <配置文件路径>")
        print("示例: python configure_switch_h3c.py switch_config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    main(config_file)
