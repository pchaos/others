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

import shutil
import requests
import re
from run_limited import limit_calls, limit_calls_with_waiting


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def resolve_ip_address(ip_address):
    """
    Resolve an IP address to its corresponding address if it's a domain.

    Args:
        ip_address (str): The IP address or domain to resolve.

    Returns:
        str: The resolved IP address or the original if it's already an IP.
    """
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if not re.match(ip_pattern, ip_address):
        try:
            res = dns_resolver.Resolver()
            answer = res.resolve(ip_address, "A")
            for record in answer:
                return record.address
        except dns.resolver.NXDOMAIN:
            logger.error(f"Domain {ip_address} does not exist.")
        except dns.resolver.NoAnswer:
            logger.error(f"No answer for IP {ip_address}.")
        except dns.resolver.Timeout:
            logger.error(f"Timeout for IP {ip_address}.")
        except Exception as e:
            logger.error(f"Error looking up country for IP {ip_address}: {str(e)}")
    return ip_address  # Return original if it's already an IP or if an error occurred

def download_geoip_database(db_path):
    """
    Download the GeoIP database if it does not exist or is smaller than 1MB.

    Args:
        db_path (str): The path where the GeoIP database should be stored.

    Returns:
        bool: True if the database was downloaded successfully, False otherwise.
    """
    logger.info("GeoIP database not found. Attempting to download...")
    url = "https://github.com/P3TERX/GeoLite.mmdb/raw/main/GeoLite2-Country.mmdb"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            if int(response.headers.get('Content-Length', 0)) < 1024 * 1024:  # Check if file size is greater than 1MB
                logger.error("GeoIP database file size exceeds 1MB limit.")
                return False
            else:
                with open(db_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
                logger.info("GeoIP database downloaded successfully.")
                return True
        else:
            logger.error(f"Failed to download GeoIP database. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error downloading GeoIP database: {str(e)}")
        return False

@limit_calls_with_waiting(max_calls=45, period=60)
def get_country_from_api(ip_address):
    """
    Get the country of an IP address using the ip-api.com service.

    Args:
        ip_address (str): The IP address to look up.

    Returns:
        str: The country name if found, otherwise 'Unknown'.
    """
    # 使用ip-api.com查询IP地址 使用限制: 每分钟限制45个IP地址请求，超限将限流
    url = "http://ip-api.com/json/" + ip_address
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        return data.get('country', 'Unknown')
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return 'Unknown'
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Error connecting to the API: {conn_err}")
        return 'Unknown'
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return 'Unknown'
    except requests.exceptions.RequestException as err:
        logger.error(f"Request error occurred: {err}")
        return 'Unknown'

def get_country_from_geoip(ip_address):
    """
    Get the country of an IP address using the GeoIP2 database.

    Args:
        ip_address (str): The IP address to look up.

    Returns:
        str: The country name if found, otherwise 'Unknown'.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'GeoLite2-Country.mmdb')

    if not os.path.exists(db_path) or os.path.getsize(db_path) < 1024 * 1024:
        if not download_geoip_database(db_path):
            print(f"GeoIP database not found at {db_path}")
            return 'Unknown'

    try:
        with geoip2.database.Reader(db_path) as reader:
            # todo response.country.nname返回不正确
            response = reader.country(ip_address=ip_address)
            return response.country.name or 'Unknown'
    except geoip2.errors.AddressNotFoundError:
        return 'Unknown'
    except Exception as e:
        print(f"Error looking up country for IP {ip_address}: {str(e)}")
        return 'Unknown'

def get_country_from_ip(ip_address, online_check=True):
    """
    Retrieve the country associated with an IP address using the GeoIP2 database and online API.

    Args:
        ip_address (str): The IP address to look up.
        online_check (bool, optional): Flag to enable online API lookup if GeoIP2 fails. Defaults to True.

    Returns:
        str: The country name if found, otherwise 'Unknown'.

    Note:
        This function requires the GeoIP2 database file (GeoLite2-Country.mmdb).
        If the file is not present, it will be downloaded from a mirror site.
        Online API lookup is used as a fallback if GeoIP2 lookup fails and online_check is True.
    """
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if not re.match(ip_pattern, ip_address):
        ip_address = resolve_ip_address(ip_address)
    country = get_country_from_geoip(ip_address)
    if country == 'Unknown' and online_check:
        country = get_country_from_api(ip_address)
    return country

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
            res.timeout = 3  # 设置超时时间为5秒
            res.lifetime = 3  # 设置查询生命周期为5秒
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
                answers = res.query(qname, 'A')
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

# This function has been moved to dns_check.py
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
    dns_list = ["8.8.8.8", "1.0.0.1", "208.67.222.222", "192.168.100.1","192.168.1.1", "11.2.3.4","203.125.192.179", "116.12.188.65"]
    # available_dns = check_dns_availability(dns_list)
    available_dns= check_dns_availability_query(dns_list, qname="www.amazon.com")
    print("可用的DNS地址:", available_dns)
    print("不可用的DNS地址:", [dns for dns in dns_list if dns not in available_dns])