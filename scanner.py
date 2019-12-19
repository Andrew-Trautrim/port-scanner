#!/usr/bin/python
import socket
import sys
from datetime import datetime

def main():
    t1 = datetime.now
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + "<target address>"
        exit()
    
    addr = sys.argv[1]

t1 = datetime.now()
main()
t2 = datetime.now()
print "Scanning completed in ", t2 - t1
