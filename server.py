import config
from ftp_server_class import FtpServer
from router import SimpleRouter
from server_class import Server


def waiting_msg(sock_server: Server, router: SimpleRouter):
    while True:
        answer = router.execute(sock_server.receive())
        sock_server.send(answer)


if __name__ == '__main__':
    router = SimpleRouter()
    thread_ftp_server = FtpServer(config.HOST, config.FTP_PORT, config.FTP_USER, config.FTP_PASSWORD)
    thread_ftp_server.run()
    sock_server = Server(config.HOST, config.PORT)
    waiting_msg(sock_server, router)
