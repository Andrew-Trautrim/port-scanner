#!/usr/bin/python
import os
import platform
import socket
import sys
from datetime import datetime

# pings the address to determine if the host is up
def ping(addr):
    system = platform.system()
    if (system == "Windows"):
        cmd = "ping -n 1 "
    else:
        cmd = "ping -c 1 -W 2 "

    response = os.popen(cmd + addr)
    for line in response.readlines():
        if "ttl" in line:
            return True
    return False

# scans port via a tcp connection
def scan(addr, port):
    socket.setdefaulttimeout(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((addr, port))
    s.close()
    if  result == 0:
        return True # returns true if the port is open
    else:
        return False # false otherwise

def get_range(ip_range):
    net = ip_range.split('-')
    if (len(net) == 1):
        return (int(net[0]), int(net[0])+1)
    return (int(net[0]), int(net[1])+1)

def main():
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + "<target address>"
        exit()
    
    addr = sys.argv[1]
    addrs = addr.split('.')
    if len(addrs) != 4:
        print "invalid address"
        exit()

    (s1,e1) = get_range(addrs[0])
    (s2,e2) = get_range(addrs[1])
    (s3,e3) = get_range(addrs[2])
    (s4,e4) = get_range(addrs[3])

    t1 = datetime.now()
    print "Scanning..."
    for b1 in range(s1, e1):
        for b2 in range(s2, e2):
            for b3 in range(s3, e3):
                for b4 in range(s4, e4):
                    target = str(b1) + '.' + str(b2) + '.' + str(b3) + '.' + str(b4)
                    if ping(target):
                        print target, "is up"
                        print "Port 80:  " + ("OPEN" if scan(target, 80) else "CLOSED")
                        print "Port 443: " + ("OPEN" if scan(target, 443) else "CLOSED")
                        print ""
                    else:
                        print target, "is down"
                        print ""

    t2 = datetime.now()
    print "Scanning completed in ", t2 - t1

main()
