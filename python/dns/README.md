# DNS Check Tool

Python 工具集，用于 DNS 服务器可用性检测、IP 地理位置查询及调用频率限制。

## 功能

- **DNS 可用性检测** — 批量测试 DNS 服务器是否可用（支持 TCP/UDP 模式、自动 DDR 发现）
- **IP 地理位置查询** — 通过 GeoLite2 本地数据库 + ip-api.com 在线 API 双重查询 IP 所属国家
- **域名解析** — 将域名解析为 IP 地址
- **调用频率限制** — 可复用的装饰器，限制函数在指定时间窗口内的调用次数（支持静默拒绝和自动等待两种模式）
- **网页 DNS 抓取** — 基于 SeleniumBase 从 dns.supfree.net 抓取新加坡 DNS 地址并验证

## 文件结构

```
dns/
├── dns_check.py          # 核心模块：DNS 检测、IP 地理查询、域名解析
├── run_limited.py        # 调用频率限制装饰器
├── test_dns_check.py     # dns_check.py 单元测试
├── test_run_limited.py   # run_limited.py 单元测试
├── test_get_dns.py       # SeleniumBase 网页 DNS 抓取测试
├── pytest.ini            # pytest 配置
├── GeoLite2-Country.mmdb # MaxMind GeoLite2 国家数据库
├── GeoLite2-City.mmdb    # MaxMind GeoLite2 城市数据库
└── GeoLite2-ASN.mmdb     # MaxMind GeoLite2 ASN 数据库
```

## 依赖

```
dnspython       # DNS 解析
geoip2          # GeoIP 数据库读取
requests        # HTTP 请求
seleniumbase    # 网页自动化（仅 test_get_dns.py 需要）
pytest          # 测试框架
```

未安装时 `dns_check.py` 会自动尝试 pip 安装 `dnspython` 和 `geoip2`。

## 使用方法

### DNS 可用性检测

```python
from dns_check import check_dns_availability

dns_list = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
available = check_dns_availability(dns_list, qname="www.amazon.com", tcp=True)
print(available)  # ['8.8.8.8', '1.1.1.1']
```

### IP 地理查询

```python
from dns_check import get_country_from_ip

# 支持 IP 和域名
country = get_country_from_ip("1.0.0.1")              # Australia
country = get_country_from_ip("www.mfa.gov.sg")       # 自动解析域名后查询
country = get_country_from_ip("8.8.8.8", online_check=False)  # 仅本地数据库
```

### 调用频率限制

```python
from run_limited import limit_calls, limit_calls_with_waiting

# 模式 1: 超限后返回 None
@limit_calls(max_calls=45, period=60)
def my_function():
    pass

# 模式 2: 超限后自动等待直到下一个周期
@limit_calls_with_waiting(max_calls=45, period=60)
def my_function():
    pass
```

## 运行测试

```bash
# 全部测试
pytest

# 指定模块
pytest test_dns_check.py
pytest test_run_limited.py

# 指定单个测试
pytest test_dns_check.py::TestDNSCheck::test_get_country_from_ip
```

## 直接运行

```bash
python dns_check.py      # 使用内置 DNS 列表进行可用性检测
```

## 数据库

项目内置 MaxMind GeoLite2 数据库（Country / City / ASN）。如本地数据库缺失或小于 1MB，`dns_check.py` 会自动从 [P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb) 镜像下载。

## 注意事项

- `get_country_from_api` 使用 ip-api.com，受每分钟 45 次请求限制，已通过 `limit_calls_with_waiting` 装饰器自动限流
- `check_dns_availability` 默认使用 TCP 模式查询，TCP 失败时会自动对无响应服务器回退到 UDP 重试
- `test_get_dns.py` 需要 Chrome 浏览器及 SeleniumBase 环境
