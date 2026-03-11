#!/usr/bin/env python3
"""
CF优选域名测试脚本
测试域名对应的IP连通性和速度
"""

import ipaddress
import json
import random
import socket
import ssl
import string
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# 配置
TIMEOUT = 5  # 超时时间(秒)
SAMPLE_IPS = 2  # 每个域名随机抽取的IP数量
MAX_WORKERS = 10  # 并发数
MAX_DOMAINS = 0  # 测试域名数量限制（0=全部）

# Cloudflare IP段缓存
_CF_IP_RANGES = None


def get_cloudflare_ip_ranges() -> list:
    """从Cloudflare API获取IP段"""
    try:
        with urllib.request.urlopen(
            "https://api.cloudflare.com/client/v4/ips", timeout=5
        ) as response:
            data = json.loads(response.read().decode())
            return data.get("result", {}).get("ipv4_cidrs", [])
    except Exception:
        return [
            "173.245.48.0/20",
            "103.21.244.0/22",
            "103.22.200.0/22",
            "103.31.4.0/22",
            "141.101.64.0/18",
            "108.162.192.0/18",
            "190.93.240.0/20",
            "188.114.96.0/20",
            "197.234.240.0/22",
            "198.41.128.0/17",
            "162.158.0.0/15",
            "104.16.0.0/13",
            "104.24.0.0/14",
            "172.64.0.0/13",
            "131.0.72.0/22",
        ]


def is_cloudflare_ip(ip: str) -> bool:
    """判断IP是否属于Cloudflare"""
    global _CF_IP_RANGES
    if _CF_IP_RANGES is None:
        _CF_IP_RANGES = [
            ipaddress.ip_network(cidr) for cidr in get_cloudflare_ip_ranges()
        ]

    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in network for network in _CF_IP_RANGES)
    except Exception:
        return False


def process_wildcard_domain(domain: str) -> str:
    """处理通配符域名，将*替换为随机字母或数字"""
    if "*" not in domain:
        return domain

    result = []
    for char in domain:
        if char == "*":
            result.append(random.choice(string.ascii_lowercase + string.digits))
        else:
            result.append(char)
    return "".join(result)


def load_domains(yaml_path: str) -> list:
    """从YAML文件读取域名列表"""
    import yaml

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    domain_list = data.get("CF优选域名", [])
    for item in domain_list:
        if "list" in item:
            return item["list"]
    return []


def resolve_ips(domain: str) -> list:
    """DNS解析获取域名的所有IP"""
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET)
        ips = list(set([r[4][0] for r in results]))
        return ips
    except socket.gaierror:
        return []


def test_ping(ip: str) -> dict:
    """测试Ping延迟和丢包率"""
    try:
        result = subprocess.run(
            ["ping", "-c", "3", "-W", str(TIMEOUT), ip],
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 3,
        )

        rtt = 0
        loss = 100

        for line in result.stdout.split("\n"):
            if "packet loss" in line:
                try:
                    loss = int(line.split("%")[0].strip().split()[-1])
                except:
                    pass
            if "rtt min/avg/max/mdev" in line or "rtt min/avg/max" in line:
                try:
                    avg = line.split("=")[1].split("/")[1]
                    rtt = float(avg)
                except:
                    pass

        return {"success": loss < 100, "rtt": rtt, "loss": loss}
    except Exception as e:
        return {"success": False, "rtt": None, "loss": 100}


def test_domain_tls(domain: str, ip: str) -> dict:
    """使用TLS握手测试域名访问(带SNI)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        ssl_sock = context.wrap_socket(sock, server_hostname=domain)
        ssl_sock.connect((ip, 443))

        request = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
        ssl_sock.sendall(request.encode())

        response = b""
        while True:
            data = ssl_sock.recv(4096)
            if not data:
                break
            response += data
            if b"\r\n\r\n" in response:
                break

        ssl_sock.close()

        response_str = response.decode("utf-8", errors="ignore")
        status_line = response_str.split("\r\n")[0]

        if "HTTP/" in status_line:
            status_parts = status_line.split()
            if len(status_parts) >= 2:
                status_code = int(status_parts[1])
                return {
                    "success": status_code >= 200 and status_code < 400,
                    "status": status_code,
                    "headers_received": True,
                }

        return {"success": True, "status": 200, "headers_received": True}

    except Exception as e:
        return {"success": False, "status": 0, "error": str(e)}


def test_domain(domain: str) -> dict:
    """测试单个域名的所有IP"""

    # 处理通配符域名
    original_domain = domain
    test_domain = process_wildcard_domain(domain)

    result = {
        "domain": original_domain,
        "test_domain": test_domain,
        "ips": [],
        "sample_ips": [],
        "cf_sni_supported": None,
        "cf_sni_status": None,
    }

    # 使用处理后的域名进行DNS解析和测试
    all_ips = resolve_ips(test_domain)
    if not all_ips:
        result["error"] = "DNS解析失败"
        result["cf_sni_supported"] = None
        result["cf_sni_status"] = "dns_failed"
        return result

    result["ips"] = all_ips

    cf_ips = [ip for ip in all_ips if is_cloudflare_ip(ip)]
    if not cf_ips:
        result["cf_sni_supported"] = False
        result["cf_sni_status"] = "not_cf_ip"

    sample_count = min(SAMPLE_IPS, len(all_ips))
    sample_ips = random.sample(all_ips, sample_count)
    result["sample_ips"] = sample_ips

    results = []
    tls_all_failed = True

    for ip in sample_ips:
        ip_result = {"ip": ip}

        ping_result = test_ping(ip)
        ip_result["ping"] = ping_result

        # TLS测试使用处理后的域名
        tls_result = test_domain_tls(test_domain, ip)
        ip_result["domain_tls"] = tls_result

        if tls_result.get("success"):
            tls_all_failed = False

        results.append(ip_result)

    result["test_results"] = results

    if cf_ips:
        if tls_all_failed:
            result["cf_sni_supported"] = False
            result["cf_sni_status"] = "tls_failed"
        else:
            result["cf_sni_supported"] = True
            result["cf_sni_status"] = "ok"

    return result


def main():
    """主函数"""
    script_dir = Path(__file__).parent
    yaml_path = script_dir / "CF优选域名.yaml"
    output_path = script_dir / "cf_test_results.json"

    print("=" * 50)
    print("CF优选域名连通性测试 (域名SNI版)")
    print("=" * 50)

    print(f"\n[1/4] 加载Cloudflare IP段...")
    cf_ranges = get_cloudflare_ip_ranges()
    print(f"     已加载 {len(cf_ranges)} 个IPv4段")

    print(f"\n[2/4] 读取域名列表...")
    domains = load_domains(str(yaml_path))

    if MAX_DOMAINS > 0:
        domains = domains[:MAX_DOMAINS]

    print(f"     共有 {len(domains)} 个域名")

    print(f"\n[3/4] 开始测试 (并发: {MAX_WORKERS}, 超时: {TIMEOUT}s)")
    print(f"     符号说明: [TLS连接] [CF套SNI] ✓=成功 ✗=失败 ?=未知")
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(test_domain, d): d for d in domains}

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)

            has_available = False
            if "test_results" in result:
                for ip_result in result["test_results"]:
                    if ip_result.get("domain_tls", {}).get("success"):
                        has_available = True
                        break

            cf_sni = result.get("cf_sni_supported")
            cf_sni_str = "✓" if cf_sni else "✗" if cf_sni is False else "?"

            status = "✓" if has_available else "✗"
            domain = result.get("domain", "unknown")
            print(f"     [{i + 1}/{len(domains)}] {status}{cf_sni_str} {domain}")

    results.sort(key=lambda x: x["domain"])

    print(f"\n[4/4] 统计结果")

    total_domains = len(results)
    total_ips = sum(len(r.get("ips", [])) for r in results)

    available_ips = 0
    cf_sni_available = 0

    for r in results:
        if "test_results" in r:
            for ip_result in r["test_results"]:
                if ip_result.get("domain_tls", {}).get("success"):
                    available_ips += 1

        if r.get("cf_sni_supported") == True:
            cf_sni_available += 1

    print(f"     域名总数: {total_domains}")
    print(f"     IP总数: {total_ips}")
    print(f"     可用IP: {available_ips}")
    print(f"     CF套SNI可用: {cf_sni_available}")

    output = {
        "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_domains": total_domains,
        "total_ips": total_ips,
        "available_ips": available_ips,
        "cf_sni_available": cf_sni_available,
        "results": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存: {output_path}")

    print("\n" + "=" * 50)
    print("可用的IP (域名TLS访问成功)")
    print("=" * 50)

    ip_groups = {}
    for r in results:
        if "test_results" in r:
            for ip_result in r["test_results"]:
                if ip_result.get("domain_tls", {}).get("success"):
                    ip = ip_result["ip"]
                    ping = ip_result.get("ping", {})
                    rtt = ping.get("rtt", 0)

                    if ip not in ip_groups:
                        ip_groups[ip] = []
                    ip_groups[ip].append((r["domain"], rtt))

    sorted_ips = sorted(
        ip_groups.keys(), key=lambda ip: min(item[1] for item in ip_groups[ip])
    )

    for ip in sorted_ips:
        items = ip_groups[ip]
        items.sort(key=lambda x: x[1])
        formatted = ", ".join([f"{domain} ({rtt:.0f}ms)" for domain, rtt in items])
        print(f"{ip} - {formatted}")

    print(f"\n总共 {len(sorted_ips)} 个独立IP")

    # 生成hosts文件
    print("\n" + "=" * 50)
    print("生成hosts文件")
    print("=" * 50)

    # 筛选支持CF套SNI的域名，按延迟排序
    cf_sni_ips = []
    for r in results:
        if r.get("cf_sni_supported") == True and "test_results" in r:
            for ip_result in r["test_results"]:
                if ip_result.get("domain_tls", {}).get("success"):
                    ip = ip_result["ip"]
                    ping = ip_result.get("ping", {})
                    rtt = ping.get("rtt", 0)
                    cf_sni_ips.append((ip, rtt))

    # 按延迟排序并去重
    cf_sni_ips.sort(key=lambda x: x[1])
    unique_ips = []
    seen = set()
    for ip, rtt in cf_sni_ips:
        if ip not in seen:
            seen.add(ip)
            unique_ips.append((ip, rtt))

    if unique_ips:
        hosts_path = Path("/tmp/30_cf.hosts")
        with open(hosts_path, "w", encoding="utf-8") as f:
            fastest_rtt = unique_ips[0][1]

            if fastest_rtt < 100:
                f.write(f"{unique_ips[0][0]} speeds.firefox.com\n")
                speeds_ips = [unique_ips[0]]
                speeds_label = (
                    f"最快IP < 100ms: {unique_ips[0][0]} ({fastest_rtt:.0f}ms)"
                )
            else:
                for ip, rtt in unique_ips[:2]:
                    f.write(f"{ip} speeds.firefox.com\n")
                speeds_ips = unique_ips[:2]
                speeds_label = f"最快IP >= 100ms: 前2个IP"

            for ip, rtt in unique_ips[:3]:
                f.write(f"{ip} sxsc.dpdns.org\n")

        print(f"hosts文件已保存: {hosts_path}")
        print(f"  {speeds_label} -> speeds.firefox.com")
        for i, (ip, rtt) in enumerate(unique_ips[:3], 1):
            print(f"  #{i}: {ip} ({rtt:.0f}ms) -> sxsc.dpdns.org")
    else:
        print("  无支持CF套SNI的可用IP")


if __name__ == "__main__":
    main()
