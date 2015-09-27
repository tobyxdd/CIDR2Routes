__author__ = 'tobyx'

import sys
from netaddr import *

upt = "@echo off\nfor /F \"tokens=3\" %%* in ('route print ^| findstr \"\\<0.0.0.0\\>\"') do set \"gw=%%*\"\nIF %gw%==%%* (\n  echo \u9519\u8BEF: \u672A\u80FD\u627E\u5230\u7F51\u5173\n  pause\n  exit\n)\nipconfig /flushdns\n"
downt = "@echo off\n"

argf = sys.argv[1]
with open(argf) as cf:
    cidrs = [line.rstrip('\n') for line in cf]
    ipcount = 0
    for cidr in cidrs:
        ipn = IPNetwork(cidr)
        upt += "route add " + str(ipn.ip) + " mask " + str(ipn.netmask) + " %gw% metric 5\n"
        downt += "route delete " + str(ipn.ip) + "\n"
        ipcount += ipn.size
    with open(argf + "_up.bat", "w") as upf, open(argf + "_down.bat", "w")as dnf:
        upf.write(upt)
        dnf.write(downt)
    print("Done. " + str(ipcount) + " IPs in total.")
