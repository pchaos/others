import pandas as pd

import numpy as np

import requests
# pip install pysocks

import time
import json

def user_proxy(proxies, url):
    import urllib.request
    proxy = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data

# 真实ip
my_ip = json.loads(requests.get("https://httpbin.org/ip").text)["origin"]
print('默认公网ip： {}'.format(my_ip))

checkip = 'https://icanhazip.com/'
checkip = 'http://www.whatsmyip.net/'
checkip = 'http://whatismyip.akamai.com'
checkip = 'http://jsonip.com'

TMP_EFFECTIVE_IP_CSV = '/tmp/effective_ip.csv'

df = pd.read_csv('/tmp/ip.csv', header=None, names=["ip", "port", "anonymous", "proxy_type", "speed"])

proxy_types = ["{}".format(i) for i in np.array(df['proxy_type'])]

ips = ["{}".format(i) for i in np.array(df['ip'])]

ports = ["{}".format(i) for i in np.array(df['port'])]

proxy_url = ['{0}://{1}:{2}'.format(proxy_types[i], ips[i], ports[i]) for i in range(len(ips))]
# proxy_url = ['{}:{}'.format(ips[i], ports[i]) for i in range(len(ips))]

proxy_type = ['{}'.format(i) for i in proxy_types]

# for i in range(df.ip.count()):
for i in range(10):

    time.sleep(0.1)
    proxies = {
        proxy_type[i]: proxy_url[i]
        # 'HTTP': proxy_url[i],
        # 'HTTPS': proxy_url[i],

    }
    try:
        # rs = requests.get(checkip, proxies=proxies, timeout=5, verify=False)
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5://localhost:9150'
        session.proxies['https'] = 'socks5://localhost:9150'
        # session.proxies['http'] = proxy_url[i]
        # session.proxies['https'] = proxy_url[i]
        # session.proxies = proxies
        rs = session.get('http://httpbin.org/ip')

    except Exception as e:
        print('invalid ip and port: {}'.format(e.args))
    else:
        code = rs.status_code
        if code == 200:
            # rscontent = user_proxy(proxies, checkip)
            rscontent = rs.text
            print('{} effective ip: {} {} {}, ||{}||'.format(i, ips[i], ports[i], proxy_type[i], rscontent))
            if ips[i] in rscontent:
                with open(TMP_EFFECTIVE_IP_CSV, 'a+', encoding='utf-8-sig') as f:
                    f.write(proxy_type[i] + ',' + proxy_url[i] + '\n')
        else:
            print('invalid ip and port')

print('Done!')