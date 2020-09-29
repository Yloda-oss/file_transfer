#self.server_ip = self.get_server_ip()
#self.client = self.connect_to_server(self.get_server_ip())
#self.Ftp_client = self.connect_to_ftp_server()
import json
d = {'args': 'arg',
     'i': 1}
print(d)
print(str(d))
print(json.dumps(str(d)))
print(json.dumps(d))
