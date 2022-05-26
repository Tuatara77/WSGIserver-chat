import wsgiserver


class Server:
    def __init__(self, port:int=8000):
        self.sep = "|<SEPARATOR>|"
        self.paths = wsgiserver.WSGIPathInfoDispatcher({
            "/": self._main,
            "/send": self._receive,
            "/get": self._send
        })
        self.server = wsgiserver.WSGIServer(self.paths, port=port)
        self.data = []
    
    def start(self):
        """Starts the server"""
        self.server.start()

    def stop(self):
        """Stops the server"""
        self.server.stop()

    def _main(self, environ, start_response):
        """Main page, appears as a gateway error"""
        start_response("503 ok", [('Content-type','text/plain')])
        yield b""
    
    def _receive(self, environ, start_response):
        """Server is RECEIVING data"""
        data = environ["PATH_INFO"][1:]
        if data:
            self.data.append(data)
            start_response("503 ok", [('Content-type','text/plain')])
        else: start_response("503 ok", [('Content-type','text/plain')])
        yield b""

    def _send(self, environ, start_response):
        """Server is SENDING data"""
        start_response("503 ok", [("Content-type", "text/plain")])
        body = b""
        for f in self.data: body += bytes(f"{f}{self.sep}", "utf-8")
        yield body
