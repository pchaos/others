function FindProxyForURL (url, host) {
  // our local URLs from the domains below example.com don't need a proxy:
  if (shExpMatch(host, "*.example.com")) {
    return "DIRECT";
  }

  // URLs within this network are accessed through
  // port 8080 on fastproxy.example.com:
  if (isInNet(host, "10.0.0.0", "255.255.248.0")) {
    return "PROXY fastproxy.example.com:8080";
  }

  // All other requests go through port 1080 of fastproxy.example.com.
  // should that fail to respond, go directly to the WWW:
  return "socks5 fastproxy.example.com:1080; DIRECT";
}

// 在hosts中设置fastproxy.example.com 为代理服务器ip