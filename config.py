import socket

def get_ip():
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


HOST = get_ip()
PORT = 9090
FTP_PORT = 2121
FTP_USER = 'onmsiofnawkmdfk'
FTP_PASSWORD = 'r7894hpsg789fh8)dhsbf'
