# -*- coding=utf-8 -*-

import logging
import os

try:
    import dns.resolver as dns_resolver
    import dns
except ImportError:
    import subprocess
    import sys

    print("dnspython is not installed. Attempting to install it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "dnspython"])
    import dns.resolver

try:
    import geoip2.database
except ImportError:
    import subprocess
    import sys
    print("geoip2 is not installed. Attempting to install it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geoip2"])
    import geoip2.database

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dns_availability(dns_list, qname="www.dnspython.org", tcp=True):
    """
    检查给定的DNS列表中的DNS是否可用。

    此函数执行以下操作：
    1. 遍历提供的DNS地址列表。
    2. 对每个DNS地址进行可用性测试。
    3. 尝试解析指定的域名（默认为 www.dnspython.org）。
    4. 验证返回的IP地址是否有效。
    5. 记录每个DNS的测试结果（可用、超时、无效等）。
    6. 返回可用的DNS地址列表。

    Args:
        dns_list (List[str]): A list containing DNS server addresses to be checked.
        qname (str, optional): The domain name to be used for testing. Defaults to "www.dnspython.org".
        tcp (bool, optional): Whether to use TCP for DNS queries. Defaults to True.

    Returns:
        List[str]: A list of available DNS server addresses.

    Raises:
        None

    Note:
        - If TCP mode fails, the function will attempt to recheck using UDP mode.
        - The function handles various DNS-related exceptions such as timeouts and NXDOMAIN.
        - All test results are logged.
    """

    available_dns = []
    undetermined_dns = []
    for dns_checking in dns_list:
        try:
            res = dns_resolver.Resolver(configure=False)
            res.nameservers = [dns_checking]
            res.timeout = 5  # 设置超时时间为5秒
            res.lifetime = 5  # 设置查询生命周期为5秒
            try:
                res.try_ddr()
                answers = res.resolve(qname, 'A', tcp=tcp)
                if answers:
                    # 验证返回的IP地址是否有效
                    ip_addresses = [rdata.address for rdata in answers]
                    if any(ip_address for ip_address in ip_addresses):
                        available_dns.append(dns_checking)
                        logger.info(f"DNS {dns_checking} returned IP(s): {', '.join(ip_addresses)}")
                    else:
                        logger.warning(f"DNS {dns_checking} returned invalid IP(s)")
            except dns.exception.Timeout:
                logger.warning(f"DNS {dns_checking} timed out")
            except dns_resolver.NXDOMAIN:
                logger.warning(f"DNS {dns_checking} returned NXDOMAIN")
            except dns_resolver.NoNameservers:
                logger.warning(f"DNS {dns_checking} has no available nameservers")
                if tcp:
                    undetermined_dns.append(dns_checking)
            except dns.exception.DNSException as e:
                logger.warning(f"DNS {dns_checking} raised an exception: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error with DNS {dns_checking}: {str(e)}")
    if tcp and len(undetermined_dns) > 0:
        second_check_dns = check_dns_availability(undetermined_dns, qname=qname, tcp=False)
        if len(second_check_dns) > 0:
            available_dns.extend(second_check_dns)
    return available_dns

def check_dns_availability_query(dns_list, qname="www.dnspython.org"):
    """
    使用dns.resolver.query检查给定的DNS列表中的DNS是否可用。

    此函数执行以下操作：
    1. 遍历提供的DNS地址列表。
    2. 对每个DNS地址进行可用性测试。
    3. 尝试解析指定的域名（默认为 www.dnspython.org）。
    4. 验证返回的IP地址是否有效。
    5. 记录每个DNS的测试结果（可用、超时、无效等）。
    6. 返回可用的DNS地址列表。

    Args:
        dns_list (List[str]): A list containing DNS server addresses to be checked.
        qname (str, optional): The domain name to be used for testing. Defaults to "www.dnspython.org".

    Returns:
        List[str]: A list of available DNS server addresses.

    Raises:
        None

    Note:
        - The function handles various DNS-related exceptions such as timeouts and NXDOMAIN.
        - All test results are logged.
    """

    available_dns = []
    for dns_checking in dns_list:
        try:
            res = dns_resolver.Resolver(configure=False)
            res.nameservers = [dns_checking]
            res.timeout = 5  # 设置超时时间为5秒
            res.lifetime = 5  # 设置查询生命周期为5秒
            try:
                res.try_ddr()
                answers = dns_resolver.query(qname, 'A')
                if answers:
                    # 验证返回的IP地址是否有效
                    ip_addresses = [rdata.address for rdata in answers]
                    if any(ip_address for ip_address in ip_addresses):
                        available_dns.append(dns_checking)
                        logger.info(f"DNS {dns_checking} returned IP(s): {', '.join(ip_addresses)}")
                    else:
                        logger.warning(f"DNS {dns_checking} returned invalid IP(s)")
            except dns.exception.Timeout:
                logger.warning(f"DNS {dns_checking} timed out")
            except dns_resolver.NXDOMAIN:
                logger.warning(f"DNS {dns_checking} returned NXDOMAIN")
            except dns_resolver.NoNameservers:
                logger.warning(f"DNS {dns_checking} has no available nameservers")
            except dns.exception.DNSException as e:
                logger.warning(f"DNS {dns_checking} raised an exception: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error with DNS {dns_checking}: {str(e)}")
    return available_dns

def get_country_from_ip(ip_address):
    """
    Get the country of an IP address using the GeoLite2 database.

    Args:
        ip_address (str): The IP address to look up.

    Returns:
        str: The country name, or 'Unknown' if not found.
    """
    try:
        # Download GeoLite2-Country.mmdb from a China-accessible mirror
        import requests
        import shutil

        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'GeoLite2-Country.mmdb')

        if not os.path.exists(db_path):
            url = "https://gitee.com/mirrors/GeoLite2-Country/raw/master/GeoLite2-Country.mmdb"
            response = requests.get(url, stream=True)
            logger.info(f"Downloading GeoLite2-Country.mmdb from {url} to {db_path}")
            if response.status_code == 200:
                with open(db_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
            else:
                logger.error(f"Failed to download GeoLite2-Country.mmdb: HTTP {response.status_code}")
        
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip_address)
            return response.country.name
    except Exception as e:
        logger.error(f"Error getting country for IP {ip_address}: {str(e)}")
        return 'Unknown'

def check_dns_availability_with_country(dns_list, qname="www.dnspython.org"):
    """
    Check the availability of DNS servers and determine their countries.

    This function extends the original check_dns_availability function by adding
    country information for each available DNS server.

    Args:
        dns_list (List[str]): A list containing DNS server addresses to be checked.
        qname (str, optional): The domain name to be used for testing. Defaults to "www.dnspython.org".

    Returns:
        List[Dict]: A list of dictionaries containing available DNS server addresses and their countries.
    """
    available_dns = []
    for dns_checking in dns_list:
        try:
            res = dns_resolver.Resolver(configure=False)
            res.nameservers = [dns_checking]
            res.timeout = 5
            res.lifetime = 5
            try:
                res.try_ddr()
                answers = dns_resolver.query(qname, 'A')
                if answers:
                    ip_addresses = [rdata.address for rdata in answers]
                    if any(ip_address for ip_address in ip_addresses):
                        country = get_country_from_ip(dns_checking)
                        available_dns.append({
                            'ip': dns_checking,
                            'country': country
                        })
                        logger.info(f"DNS {dns_checking} (Country: {country}) returned IP(s): {', '.join(ip_addresses)}")
                    else:
                        logger.warning(f"DNS {dns_checking} returned invalid IP(s)")
            except dns.exception.Timeout:
                logger.warning(f"DNS {dns_checking} timed out")
            except dns_resolver.NXDOMAIN:
                logger.warning(f"DNS {dns_checking} returned NXDOMAIN")
            except dns_resolver.NoNameservers:
                logger.warning(f"DNS {dns_checking} has no available nameservers")
            except dns.exception.DNSException as e:
                logger.warning(f"DNS {dns_checking} raised an exception: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error with DNS {dns_checking}: {str(e)}")
    return available_dns

if __name__ == "__main__":
    dns_list = ["8.8.8.8", "1.1.1.1", "208.67.222.222", "192.168.100.1","192.168.1.1", "11.2.3.4","203.125.192.179", "116.12.188.65"]
    # available_dns = check_dns_availability(dns_list)
    available_dns= check_dns_availability_query(dns_list, qname="www.amazon.com")
    print("可用的DNS地址:", available_dns)
    print("不可用的DNS地址:", [dns for dns in dns_list if dns not in available_dns])