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

    print "Scanning..."
    response = os.popen(cmd + addr)
    for line in response.readlines():
        if "ttl" in line:
            return True
    return False

# scans port via a tcp connection
def scan(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = s.connect_ex((addr, port))
    if  result == 0:
        return True
    else:
        return False

def main():
    t1 = datetime.now()
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + "<target address>"
        exit()
    
    addr = sys.argv[1]
    if ping(addr):
        print addr, "is up"
        if scan(addr, 80):
            print addr + ":80 is OPEN"
    else:
        print addr, "is down"

    t2 = datetime.now()
    print "Scanning completed in ", t2 - t1

main()
