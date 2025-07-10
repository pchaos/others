# -*- coding=utf-8 -*-

# Modified: 2025-07-10 20:36:10
"""
配置文件转换工具使用说明
🚀 工具功能
本程序专门用于解析证券/金融类软件的服务器配置文件（如华泰证券等），自动提取以下关键配置项：

HostName01=主站1
IPAddress01=101.123.123.101
Port01=9001
→ 转换为标准化格式的服务器列表：

python
[('主站1', '101.123.123.101', 9001), ...]
"""
import os
import re


def parse_hqhost_config(config_str):
    """解析[HQHOST]配置段并转换为服务器元组列表"""
    servers = []

    # 清除空行和段标题
    cleaned = re.sub(r'^\[HQHOST\][\s\S]*?[\r\n]+', '', config_str.strip())

    # 解析键值对
    config_dict = {}
    for line in cleaned.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            config_dict[key.strip()] = value.strip()

    # 提取服务器配置
    i = 1
    while True:
        host_key = f'HostName{i:02d}'
        ip_key = f'IPAddress{i:02d}'
        port_key = f'Port{i:02d}'

        if host_key in config_dict and ip_key in config_dict and port_key in config_dict:
            try:
                servers.append((config_dict[host_key], config_dict[ip_key], int(config_dict[port_key])))
                i += 1
            except ValueError:
                print(f"格式错误: {port_key}={config_dict[port_key]} 端口值无效")
                i += 1
        else:
            break  # 没有更多服务器配置

    return servers


def convert_connect_file(file_path, encoding='gb2312'):
    """转换配置文件为服务器列表"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {file_path}")
        return []
    except UnicodeDecodeError:
        # 如果gb2312失败，尝试其他常见编码
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.readlines()
        except Exception:
            raise ValueError("无法解码文件，请确认编码格式")

        # 定位[HQHOST]段
    except Exception as e:
        print(f"处理错误: {str(e)}")
        return []
    hqhost_match = re.search(r'\[HQHOST\][\s\S]*?(?=\n\[|$)', content, re.IGNORECASE)

    if not hqhost_match:
        raise ValueError("配置文件中未找到[HQHOST]段")

    hqhost_section = hqhost_match.group(0)
    server_list = parse_hqhost_config(hqhost_section)

    return server_list


# ===== 主程序 =====
if __name__ == "__main__":
    cfg_path = "/dev/shm/temp/"
    # 输入文件路径
    config_file = os.path.join(cfg_path, "connect.txt")

    # 检查文件是否存在
    if not os.path.exists(config_file):
        print(f"错误: 配置文件不存在 - {config_file}")
    else:
        # 执行转换
        servers = convert_connect_file(config_file)

        # 输出转换结果
        print("\n转换完成，共发现{}个服务器配置:\n".format(len(servers)))
        print("hq_host = [")
        for server in servers:
            print(f"    {server},")
        print("]")

        # 额外输出验证信息
        print("\n主服务器 (PrimaryHost):", servers[13][0] if len(servers) > 13 else "无")
