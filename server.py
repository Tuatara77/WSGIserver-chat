import wsgiserver


class Server:
    def __init__(self, port:int=8000):
        self.sep = "|<SEPARATOR>|"
        self.paths = wsgiserver.WSGIPathInfoDispatcher({
            "/": self._main,
            "/send": self._download,
            "/get": self._upload
        })
        self.server = wsgiserver.WSGIServer(self.paths, port=port)
        self.data = []
    
    def start(self):
        """Starts the server"""
        self.server.start()

    def stop(self):
        """Stops the server"""
        self.server.stop()
    
    def upload(self, *data):
        """Receives data and stores it"""
        self.data.append("/".join(data))
    
    def download(self):
        """Returns the data"""
        data = b""
        for f in self.data: data += bytes(f"{f}{self.sep}", "utf-8")
        return str(data)[2:-1]

    def _main(self, environ, start_response):
        """Main page, appears as a gateway error"""
        start_response("503 ok", [('Content-type','text/plain')])
        yield b""
    
    def _download(self, environ, start_response):
        """Server is RECEIVING data"""
        data = environ["PATH_INFO"][1:]
        if data: self.data.append(data)
        start_response("503 ok", [('Content-type','text/plain')])
        yield b""

    def _upload(self, environ, start_response):
        """Server is SENDING data"""
        start_response("503 ok", [("Content-type", "text/plain")])
        body = b""
        for f in self.data: body += bytes(f"{f}{self.sep}", "utf-8")
        yield body
