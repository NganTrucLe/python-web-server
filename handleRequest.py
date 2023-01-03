import socket

class Request:
    def __init__(self):
        self._empty = True
        self._header = []
        self._content = ""
        self._request = ""
        self._method = ""
        self._path = ""

    def getRequest(self, conn):
        self.conn = ''
        conn.settimeout(5)
        try:
            self._request = conn.recv(1024).decode()
            while (self._request):
                data = conn.recv(1024).decode()
                self._request += data
        except socket.timeout:
            if not self._request:
                print("[SERVER] - No request is received")
        finally:
            self._empty = False
            requestArray = self._request.split("\r\n")
            self._header = requestArray[0].split()
            self._content = requestArray[-1]
            self.parseHeader()
            
    def parseHeader(self):
        if len(self._header) == 0 :
            return
        else:
            self._method = self._header[0]
            self._path = self._header[1]
    def get_header(self):
        return self._header
    def get_content(self):
        return self._content
    def get_method(self):
        return self._method
    def get_path(self):
        return self._path

    