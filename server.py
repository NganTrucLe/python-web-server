import socket
import threading
from handleRequest import *
from sendResponse import *

def handler(conn : socket.socket, address):
    print(f"-------------------\n [SERVER]\n {address} sent request to server.\n")
    request = Request()
    request.getRequest(conn)
    if len(request.get_header()) != 0:
        print(f"-------------------\n [SERVER]\n Request recieved")
        if request.get_method() == 'GET':
            do_GET(conn, request.get_path())
        elif request.get_method() == 'POST':
            do_POST(conn, request.get_path(), request.get_content())
    conn.close()


def main():
    host =  "localhost"
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    server.bind(('', port))
    server.listen(5)
    print(f"-------------------\n [SERVER]\n Listening on: {host} {port}")
    cnt = 1

    while 1:
        (conn, address) = server.accept()
        thread = threading.Thread(target=handler, args=(conn, address))
        print(f" Thread {cnt}\n")
        cnt += 1
        thread.start()
       

if __name__ == '__main__':
    main()