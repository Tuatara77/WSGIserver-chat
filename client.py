import http.client

class Client:
    def __init__(self, server_ip:str, server_port:int=80):
        self.ip = server_ip
        self.port = server_port

    def request(self):
        conn = http.client.HTTPConnection(f"{self.ip}:{self.port}", timeout=10)
        conn.request("GET","/get")
        r1 = conn.getresponse()
        content = r1.read()
        conn.close()
        return str(content)[2:-1]

    def send(self, *data):
        conn = http.client.HTTPConnection(f"{self.ip}:{self.port}", timeout=10)
        path = "/send"
        for f in data: path += f"/{f}"
        conn.request("SEND", path)
        conn.close()
