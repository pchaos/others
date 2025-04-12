#!/usr/bin/python
'''
    Hosts to DNSMasq configuration converter

    Converts entries in a hosts file to dnsmasq conf,
    taking wildcard into consideration.
    
    Only truncate domain name when:
        - One IP address has more than one sub-domains resolved to.
    
    USAGE: host-to-dnsmasq.py HostFile DnsmasqConfigFile
        If DnsmasqConfigFile does not exist, it will be created.
        If it exists, it will be OVERWRITTEN.
'''

import sys
import errno

def getTruncatedName(domainName):
    # Common country codes
    countryName = ["cn", "sg", "jp", "hk", "uk", "ca", "ru", "kr", "gr", "bg", "cy", \
        "fi", "co", "au", "vi", "mn", "mm", "bn", "bz", "py", "ai", "ph", "pk", "pe", \
        "pg", "ar", "tj", "na", "ng", "nf", "fj", "np", "ni", "qa", "jm", "cu", "kw", \
        "kh", "sv", "af", "sl", "ag", "sa", "sb", "pr", "ly", "tr", "tw", "lb", "et", \
        "ec", "eg", "mx", "my", "mt", "uy", "br", "pa", "bd", "bo", "bh", "vn", "vc", \
        "ua", "gt", "om", "gh", "gi", "do", "th", "ma", "mz", "ug", "ke", "ls", "nz", \
        "zm", "za", "zw", "ve", "in", "il", "id", "ao", "uz", "ck", "cr", "bw", "tz"]
    topDomains = ["com", "org", "net", "co"]

    domainElem = domainName.split(".")
    if domainElem[-1] not in countryName: # *.com
        #  return string.join(domainElem[-2:], ".")
        return f"{domainElem[-2:]}."
    else:
        if domainElem[-2] not in topDomains: # *.jp
           #  return string.join(domainElem[-2:], ".")
           return f"{domainElem[-2:]}."
        else: # *.co.uk
           #  return string.join(domainElem[-3:], ".")
            return f"{domainElem[-3:]}."

# addressMap: (address, set:[domain1, domain2, ..])
def processLine(line, address_map):
    line = line.strip();
    if line.startswith("#") or line == "":
        return # Skip comments and empty line
    else:
        lineElements = line.split()
        if len(lineElements) < 2:
            print("Malformed hosts line \"%s\", elements < 2" % line)
            exit(errno.EINVAL);
        ip = lineElements[0]
        domain = lineElements[1]
        # Ensure every IP appears in conf
        if ip not in address_map.keys():
            # first appearance of this ip
            # Do not truncate on first appearance,
            # in order to keep signle IP's domain complete
            address_map[ip] = set()
            address_map[ip].add(domain)
        else:
            # ip appeared twice+, need to truncate
            if len(address_map[ip]) == 1:
                temp_domain = address_map[ip].pop()
                address_map[ip].add(getTruncatedName(temp_domain))
            address_map[ip].add(getTruncatedName(domain))

def writeDnsmasqConf(confFile, addressMap):
    lines = []
    for (ip, domains) in addressMap.items(): # TODO why?items()
        for domain in domains:
            lines.append("address=/%s/%s\n" % (domain, ip))
    confFile.writelines(lines)

# Main program
try:
    hostFile = open(sys.argv[1], "r")
    masqFile = open(sys.argv[2], "w")
except IOError as e:
    print("ERROR: IOError, ", e)
    exit(errno.EIO)
except IndexError as e:
    print(__doc__)
    print("ERROR: Missing parameters. See Usage above.")
    exit(errno.EINVAL)
lines = hostFile.readlines()
addressMap = dict()
for line in lines:
    processLine(line, addressMap)
writeDnsmasqConf(masqFile, addressMap)
