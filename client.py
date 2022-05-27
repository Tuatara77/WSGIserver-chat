from http.client import HTTPConnection

class Client:
    def __init__(self, server_ip:str, server_port:int=80):
        self.ip = server_ip
        self.port = server_port

    def request(self):
        conn = HTTPConnection(f"{self.ip}:{self.port}", timeout=10)
        conn.request("GET","/get")
        r1 = conn.getresponse()
        content = r1.read()
        conn.close()
        return str(content)[2:-1]

    def send(self, *data):
        conn = HTTPConnection(f"{self.ip}:{self.port}", timeout=10)
        path = "/send" + "/".join(data)
        conn.request("SEND", path)
        conn.close()
