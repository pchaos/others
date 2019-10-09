function FindProxyForURL (url, host) {
  if (shExpMatch(host, "*.example.com")) {
    return "DIRECT";
  }

  if (isInNet(host, "10.0.0.0", "255.255.248.0")) {
    return "PROXY 192.168.103.1:8080";
  }

  return "socks5 192.168.103.1:1080; DIRECT";
}
