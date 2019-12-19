#!/usr/bin/python
import os
import platform
import socket
import sys
import threading
from datetime import datetime
from Queue import Queue

socket.setdefaulttimeout(1)

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
def tcp_scan(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((addr, port))
    s.close()
    if  result == 0:
        return True # returns true if the port is open
    else:
        return False # false otherwise

# performs a tcp scan if the ping returns true
def scan(addr):
    if ping(addr):
        print addr, "is up"
        print "Port 80:  " + ("OPEN" if tcp_scan(addr, 80) else "CLOSED")
        print "Port 443: " + ("OPEN" if tcp_scan(addr, 443) else "CLOSED")
        print ""
    else:
        print addr, "is down"


# determines the range in one of the 8-bit sections of the address
def get_range(ip_range):
    net = ip_range.split('-')
    if (len(net) == 1):
        return (int(net[0]), int(net[0]) + 1)
    return (int(net[0]), int(net[1]) + 1)

def main():
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + "<target address>"
        exit()
    
    addr = sys.argv[1]
    addrs = addr.split('.')
    if len(addrs) != 4:
        print "invalid address"
        exit()

    # determine ip ranges
    (s1,e1) = get_range(addrs[0])
    (s2,e2) = get_range(addrs[1])
    (s3,e3) = get_range(addrs[2])
    (s4,e4) = get_range(addrs[3])

    # threading
    print_lock = threading.Lock()

    t1 = datetime.now()
    print "Scanning..."
    for b1 in range(s1, e1):
        for b2 in range(s2, e2):
            for b3 in range(s3, e3):
                for b4 in range(s4, e4):
                    target_ip = str(b1) + '.' + str(b2) + '.' + str(b3) + '.' + str(b4)
                    t = threading.Thread(target = scan(target_ip))
                    t.daemon = True
                    t.start()

    t2 = datetime.now()
    print "Scanning completed in ", t2 - t1

main()
