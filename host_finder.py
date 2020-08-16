import os
import platform
import socket
import threading

import ipcalc
import netifaces

import config


class HostFinder:
    def __init__(self):
        self.ip = self.get_ip()
        self.current_interface = self._get_current_interface()

    def get_server(self):
        good_hosts = []

        def scan_ip(ip):
            ip = str(ip)
            comm = ping_com + ip
            response = os.popen(comm)
            data = response.readlines()
            for line in data:
                if 'TTL' in line:
                    good_hosts.append(ip)
                    break

        def get_list_ip():
            netmask = self.current_interface['netmask']
            list_ip = ipcalc.Network(self.ip, netmask)
            return list_ip

        list_ip = get_list_ip()
        system = platform.system()
        if (system == "Windows"):
            ping_com = "ping -n 1 "
        else:
            ping_com = "ping -c 1 "

        for ip in list_ip:
            if ip == self.ip:
                continue
            thread = threading.Thread(target=scan_ip, args=[ip])
            thread.start()

        thread.join()
        for ip in good_hosts:
            try:
                sock = socket.socket()
                sock.connect((ip, config.PORT))
                sock.close()
                return ip
            except:
                continue
        return None

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def _get_current_interface(self):
        interfaces_inf = None
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                for j in iface:
                    if j['addr'] == self.ip:
                        interfaces_inf = j
        return interfaces_inf


host_finder = HostFinder()
print(host_finder.get_server())
