import scapy.all
ans = scapy.all.srp(scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.all.ARP(pdst="192.168.0.0/24"),timeout=4)[0]


print([a[1].psrc for a in ans])
