import ipaddress
import socket

from pyroute2 import IPRoute
import scapy.all
import config


class HostFinder:
    def __init__(self):
        self.server = None
        self.ip = self.get_ip()
        self.network = ipaddress.ip_interface(self.get_network() + '/' + self.get_netmask())

    def get_server(self):
        answers = \
            scapy.all.srp(scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.all.ARP(pdst=self.network.network),
                          timeout=4)[
                0]
        for ip in answers:
            try:
                sock = socket.socket()
                sock.connect((ip, config.PORT))
                sock.close()
                self.server = ip
                return ip
            except:
                continue
        return None

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        return str(s.getsockname()[0])

    def get_netmask(self):
        ip = IPRoute()
        info = [{'iface': x['index'], 'addr': x.get_attr('IFA_ADDRESS'), 'mask': x['prefixlen']} for x in ip.get_addr()]
        for i in info:
            if str(i['addr']) == self.ip:
                return str(i['mask'])

    def get_network(self):
        router_ip = self.ip.split('.')
        router_ip[-1] = '1'
        router_ip = ".".join(router_ip)
        return router_ip


