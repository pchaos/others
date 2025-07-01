# app.hackthebox.com starting-point](https://app.hackthebox.com/starting-point)

<!-- vim-markdown-toc GFM -->

* [Learn the basics of Penetration Testing ](#learn-the-basics-of-penetration-testing-)
    * [tier 0](#tier-0)
        * [Meow](#meow)
        * [Fawn](#fawn)
    * [Dancing](#dancing)

<!-- vim-markdown-toc -->

## [Learn the basics of Penetration Testing ](https://app.hackthebox.com/starting-point)

### tier 0

#### Meow

Tags Telnet Protocols Reconnaissance Weak Credentials Misconfiguration

nmap -v ${ip}

telnet ${ip}

cat flag.txt

#### Fawn

    Tags: FTP Protocols Reconnaissance Anonymous/Guest Access

- What does the 3-letter acronym FTP stand for?

  File Transfer Protocol

- Which port does the FTP service listen on usually?

  21

- What does the 3-letter acronym TELNET stand for?

  sftp

- What is the command we can use to send an ICMP echo request to test our connection to the target?

  ping

- From your scans, what version is FTP running on the target?

  sFTPd 3.0.3

- From your scans, what OS type is running on the target?

  nmap -sV ${ip}
  Unix

- What is the command we need to run in order to display the 'ftp' client help menu?

  ftp -h

- What is username that is used over FTP when you want to log in without having an account?

  anonymous

- What is the response code we get for the FTP message 'Login successful'?

https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes
230

- There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system.

  ls

- What is the command used to download the file we found on the FTP server?

  get

- Submit root flag

  035db21c881520061c53e0536e44f815

### Dancing

- What port does SMB use to operate at?

  Server Message Block

- What port does SMB use to operate at?

  445

- What is the service name for port 445 that came up in our Nmap scan?

  Microsoft-DS

  Top 20 (most commonly open) TCP ports
  Port 80 (HTTP)—If you don't even know this service, you're reading the wrong book. This accounted for more than 14% of the open ports we discovered.

Port 23 (Telnet)—Telnet lives on (particularly as an administration port on devices such as routers and smart switches) even though it is insecure (unencrypted).

Port 443 (HTTPS)—SSL-encrypted web servers use this port by default.

Port 21 (FTP)—FTP, like Telnet, is another insecure protocol which should die. Even with anonymous FTP (avoiding the authentication sniffing worry), data transfer is still subject to tampering.

Port 22 (SSH)—Secure Shell, an encrypted replacement for Telnet (and, in some cases, FTP).

Port 25 (SMTP)—Simple Mail Transfer Protocol (also insecure).

Port 3389 (ms-term-server)—Microsoft Terminal Services administration port.

Port 110 (POP3)—Post Office Protocol version 3 for email retrieval (insecure).

Port 445 (Microsoft-DS)—For SMB communication over IP with MS Windows services (such as file/printer sharing).

Port 139 (NetBIOS-SSN)—NetBIOS Session Service for communication with MS Windows services (such as file/printer sharing). This has been supported on Windows machines longer than 445 has.

Port 143 (IMAP)—Internet Message Access Protocol version 2. An insecure email retrieval protocol.

Port 53 (Domain)—Domain Name System (DNS), an insecure system for conversion between host/domain names and IP addresses.

Port 135 (MSRPC)—Another common port for MS Windows services.

Port 3306 (MySQL)—For communication with MySQL databases.

Port 8080 (HTTP-Proxy)—Commonly used for HTTP proxies or as an alternate port for normal web servers (e.g. when another server is already listening on port 80, or when run by unprivileged UNIX users who can only bind to high ports).

Port 1723 (PPTP)—Point-to-point tunneling protocol (a method of implementing VPNs which is often required for broadband connections to ISPs).

Port 111 (RPCBind)—Maps SunRPC program numbers to their current TCP or UDP port numbers.

Port 995 (POP3S)—POP3 with SSL added for security.

Port 993 (IMAPS)—IMAPv2 with SSL added for security.

Port 5900 (VNC)—A graphical desktop sharing system (insecure).

Top 20 (most commonly open) UDP ports
Port 631 (IPP)—Internet Printing Protocol.

Port 161 (SNMP)—Simple Network Management Protocol.

Port 137 (NETBIOS-NS)—One of many UDP ports for Windows services such as file and printer sharing.

Port 123 (NTP)—Network Time Protocol.

Port 138 (NETBIOS-DGM)—Another Windows service.

Port 1434 (MS-SQL-DS)—Microsoft SQL Server.

Port 445 (Microsoft-DS)—Another Windows Services port.

Port 135 (MSRPC)—Yet Another Windows Services port.

Port 67 (DHCPS)—Dynamic Host Configuration Protocol Server (gives out IP addresses to clients when they join the network).

Port 53 (Domain)—Domain Name System (DNS) server.

Port 139 (NETBIOS-SSN)—Another Windows Services port.

Port 500 (ISAKMP)—The Internet Security Association and Key Management Protocol is used to set up IPsec VPNs.

Port 68 (DHCPC)—DHCP client port.

Port 520 (Route)—Routing Information Protocol (RIP).

Port 1900 (UPNP)—Microsoft Simple Service Discovery Protocol, which enables discovery of Universal plug-and-play devices.

Port 4500 (nat-t-ike)—For negotiating Network Address Translation traversal while initiating IPsec connections (during Internet Key Exchange).

Port 514 (Syslog)—The standard UNIX log daemon.

Port 49152 (Varies)—The first of the IANA-specified dynamic/private ports. No official ports may be registered from here up until the end of the port range (65536). Some systems use this range for their ephemeral ports, so services which bind a port without requesting a specific number are often allocated 49152 if they are the first program to do so.

Port 162 (SNMPTrap)—Simple Network Management Protocol trap port (An SNMP agent typically uses 161 while an SNMP manager typically uses 162).

Port 69 (TFTP)—Trivial File Transfer Protocol.

- What is the 'flag' or 'switch' that we can use with the smbclient utility to 'list' the available shares on Dancing?

  -L

  > smbclient -L ${ip}

- How many shares are there on Dancing?

  4

- What is the name of the share we are able to access in the end with a blank password?

  WorkShares

- What is the command we can use within the SMB shell to download the files we find?

  get

- Submit root flag

  5f61c10dffbc77a704d76016a22f1664

  > smbclient \\\\${ip}\WorkShares
