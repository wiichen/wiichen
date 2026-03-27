# Wiichen 项目

一个包含多种脚本和工具的综合性项目，涵盖系统运维、办公自动化、网络设备管理等领域。

---

## 项目结构

```
wiichen/
├── plane/                      # 三角形类型判断程序
├── scripts/                    # Shell 脚本（系统运维）
├── tests/                      # 测试文件
├── network_tools/              # 网络设备管理工具
├── utils/                      # 实用工具（待添加）
└── README.md                   # 项目说明文档
```

---

## 1. plane/ - 三角形类型判断程序

一个功能完善的三角形类型判断工具，支持命令行和图形界面两种模式。

### 功能特性

- **多种运行模式**：命令行版本、图形界面版本
- **三角形类型判断**：
  - 等边三角形
  - 等腰三角形
  - 普通直角三角形
  - 普通锐角三角形
  - 普通钝角三角形
  - 不能组成三角形
- **实时时间戳**：图形界面左下角显示实时时间
- **日志记录**：自动记录所有操作到日志文件
- **异常处理**：完善的输入验证和错误处理

### 文件列表

```
plane/
├── main.py              # 主入口程序
├── triangle.py          # 命令行版本
├── triangle_gui.py      # 图形界面版本
├── triangle.log         # 日志文件（自动生成）
├── minimal_triangle.py  # 精简版本
└── simple_triangle.py   # 简单版本
```

### 使用方法

#### 通过主程序运行

```bash
cd plane
python main.py
```

然后选择：
- `1` - 命令行版本
- `2` - 图形界面版本
- `3` - 运行测试
- `0` - 退出

#### 直接运行命令行版本

```bash
cd plane
python triangle.py
```

#### 直接运行图形界面版本

```bash
cd plane
python triangle_gui.py
```

### 技术说明

- **编程语言**：Python 3
- **图形界面**：tkinter
- **日志记录**：logging 标准库
- **编码格式**：UTF-8

---

## 2. scripts/ - 系统运维脚本

包含系统配置和安全加固相关的 Shell 脚本。

### 文件列表

```
scripts/
├── configure_extra.sh      # Linux网络接口配置脚本
└── reinforce_zgow_ai.sh    # 系统安全加固脚本
```

### 2.1 configure_extra.sh - Linux网络接口配置脚本

用于配置 Linux 系统网络接口的自动化脚本。

#### 功能特性

- **静态IP配置**：为指定网络接口配置静态IP地址
- **VLAN支持**：支持创建带VLAN标签的网络接口配置
- **MAC地址获取**：自动获取网络接口的MAC地址
- **UUID管理**：通过nmcli获取和管理连接UUID
- **配置文件生成**：使用here-document方式生成标准的ifcfg配置文件

#### 使用方法

```bash
cd scripts
sh configure_extra.sh <IP地址> <接口名称>
```

示例：
```bash
sh configure_extra.sh 169.15.1.1 ens2f0
```

#### 技术要点

- 使用 `ifconfig` 和 `awk` 提取MAC地址
- 使用 `nmcli` 获取网络连接的UUID
- 支持标准的Red Hat/CentOS网络配置文件格式
- 使用here-document (`<<EOF`) 生成配置文件

### 2.2 reinforce_zgow_ai.sh - 系统安全加固脚本

综合性的Linux系统安全加固工具，用于ADS-B中心系统的安全配置。

#### 功能特性

- **密码策略配置**：设置密码复杂度要求（最小长度8位，包含大小写字母、数字和特殊字符）
- **登录失败锁定**：配置连续登录失败锁定策略（10次失败，锁定300秒）
- **会话超时设置**：自动配置TMOUT=1800（30分钟超时）
- **审计规则配置**：监控/etc/passwd和/etc/shadow文件的读写执行操作
- **日志轮转**：将日志保留时间从4周调整为30周
- **用户管理**：创建多个专用用户（LESaudit、LESsafe、LESadmin、LESremote）
- **远程登录限制**：配置su命令要求wheel组权限
- **FTP安全**：禁用匿名FTP登录
- **系统日志配置**：配置远程日志服务器和本地日志文件
- **SNMP配置**：设置SNMP社区字符串
- **SSH安全加固**：禁用root登录，限制IP访问范围

#### 使用方法

```bash
cd scripts
sudo bash reinforce_zgow_ai.sh
```

#### 日志记录

- 所有操作记录到 `/tmp/reinforce_zgow.log`
- 重要配置文件自动备份（.bak后缀）
- 记录脚本开始和结束时间

#### 安全评估

**优点**：
- 覆盖多个安全领域，配置全面
- 自动化执行减少手动操作错误
- 详细的日志记录便于审计

**注意事项**：
- 需要root权限执行
- 包含硬编码密码，存在安全隐患
- 建议根据实际环境调整IP和密码配置

---

## 3. tests/ - 测试文件

包含各种测试脚本，用于验证功能正确性。

### 文件列表

```
tests/
├── test_button.py      # 按钮组件测试
├── test_simple.py      # 简单功能测试
├── test_tkinter.py     # tkinter界面测试
└── test_triangle.py    # 三角形判断程序测试
```

### 使用方法

```bash
cd tests
python test_triangle.py
```

---

## 4. network_tools/ - 网络设备管理工具集

用于华为网络设备的管理和配置工具集。

### 目录结构

```
network_tools/
├── cfg_sw/                     # 配置管理目录
│   ├── 5731_vrpcfg.cfg         # 华为设备配置文件
│   ├── ConfigHuawei.py         # 华为设备配置脚本
│   ├── ConfigHuawei_cli.py     # 华为设备命令行配置
│   ├── cfg_tem.csv             # 配置模板
│   ├── mainwindow.cpp          # C++ GUI界面
│   └── 配置模板文件.xls        # Excel配置模板
├── huawei-connect-1.py         # NETCONF连接测试
├── huawei.py                   # 华为设备能力定义
├── huaweiyang.py               # 简化能力定义
├── tcp_client.py               # TCP客户端
├── tcp_server.py               # TCP服务器
├── test.py                     # 测试脚本
├── test_export_config.py       # 配置导出测试
└── test_notification.py        # 通知测试
```

### 核心功能

#### 华为设备连接 (huawei-connect-1.py)

使用NETCONF协议连接华为设备：

```python
from ncclient import manager

def huawei_connect(host, port, user, password):
    return manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': "huaweiyang"}
    )
```

使用方法：
```bash
cd network_tools
python huawei-connect-1.py <host> <port> <username> <password>
```

#### 华为设备能力 (huawei.py / huaweiyang.py)

定义华为设备的NETCONF能力：
- execute-cli/1.0
- action/1.0
- active/1.0
- discard-commit/1.0
- exchange/1.0

#### TCP通信 (tcp_client.py / tcp_server.py)

支持Unix domain sockets的TCP客户端和服务器：

```python
# 客户端
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/tmp/uds_socket')
sock.sendall("hello server".encode())

# 服务器
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind('/tmp/uds_socket')
sock.listen(1)
```

#### 配置管理 (cfg_sw/)

- **ConfigHuawei.py**：NETCONF方式配置华为设备
- **ConfigHuawei_cli.py**：CLI命令行配置方式
- **5731_vrpcfg.cfg**：华为设备配置文件示例
- **配置模板**：标准化配置流程

### 技术栈

- **网络协议**：NETCONF、TCP/IP、Unix domain sockets
- **主要库**：ncclient（NETCONF客户端）
- **文件格式**：Python、JSON、CSV、Excel、C++

### 使用场景

1. **网络设备管理**：通过NETCONF批量配置华为网络设备
2. **配置自动化**：基于模板生成设备配置
3. **网络监控**：测试设备连接状态
4. **进程通信**：Unix domain sockets实现本地进程间通信

---

## 5. utils/ - 实用工具

待添加实用工具脚本。

---

## 项目总结

本项目包含多种脚本和工具，涵盖：

- **系统运维**：网络配置、系统安全加固
- **办公自动化**：WPS表格数据处理
- **网络设备管理**：华为设备NETCONF配置
- **通信工具**：TCP/Unix socket通信
- **算法工具**：三角形类型判断

所有脚本都采用模块化设计，便于扩展和维护。
