import wsgiserver


class Server:
    def __init__(self, port:int=8000):
        self.paths = wsgiserver.WSGIPathInfoDispatcher({
            "/": self._main,
            "/send": self._receive,
            "/get": self._send
        })
        self.server = wsgiserver.WSGIServer(self.paths, port=port)
        self.data = None
    
    def start(self):
        """Starts the server"""
        self.server.start()

    def stop(self):
        """Stops the server"""
        self.server.stop()

    def _main(self, environ, start_response):
        """Main page, appears as a gateway error"""
        body = b""
        start_response("503 ok", [('Content-type','text/plain')])
        yield body
    
    def _receive(self, environ, start_response):
        """Server is RECEIVING data"""
        data = environ["PATH_INFO"][1:]
        if data:
            body = b""
            self.data = data
            start_response("503 ok", [('Content-type','text/plain')])
            yield body
        else: start_response("503 ok", [('Content-type','text/plain')])
        
    def _send(self, environ, start_response):
        """Server is SENDING data"""
        start_response("503 ok", [("Content-type", "text/plain")])
        yield bytes(f"{self.data}", "utf-8")

