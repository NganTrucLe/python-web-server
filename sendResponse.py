import json
import os
file_map = ['/index.html', '/images.html']

def _getContentType(path : str) -> str:
    fin = open("mimeTypes.json", "r")
    mimes = json.load(fin)
    fin.close()
    return mimes["." + path.split(".")[-1]]

def _makeResponseHeader(status : str, path : str = "") -> bin:
    response = f"HTTP/1.1 {status} \r\n"
    if status == "404 Not Found" or status == "401 Unauthorized": 
        response += "Content-Type: text/html\r\n"
    else:
        response += f"Content-Type: {_getContentType(path)}\r\n"
        path = "./web_src" + path
        response += f"Content-Length: {os.stat(path).st_size}\r\n"
    response += "Connection: closed\r\n\r\n"
    return response.encode()

def _validateUser(username, password):
    fin = open("accounts.json", "r")
    accounts = json.load(fin)
    fin.close()
    if not username in accounts: 
        return False
    return accounts[username] == password

def do_GET(conn, path):
    if path == "/":
        path = "/index.html"
    if path == "/images.html":
        response = _makeResponseHeader("404 Not Found") + b"""
            <!DOCTYPE html><html>
                <head><title> 401 Unauthorized </title></head>
                <body>
                <h1>401 Unauthorized</h1>
                <p>This is a private area.</p>
                </body></html>
            """
        conn.sendall(response)
        return
    
    print(path)
    try:
        fin = open("./web_src" + path, "rb")
        response = _makeResponseHeader("200 OK", path) + fin.read()
        fin.close()
    except FileNotFoundError:
        response = _makeResponseHeader("404 Not Found") + b"""
            <!DOCTYPE html><html>
                <head><title> 404 Not Found </title></head>
                <body>
                <p>The requested file cannot be found.</p>
                </body></html>
            """
    conn.sendall(response)



def do_POST(conn, path, content):
    userInput = content.split("&")
    username = userInput[0].split("=")[1]
    password = userInput[1].split("=")[1]
    if not _validateUser(username, password):
        response = _makeResponseHeader("404 Not Found") + b"""
            <!DOCTYPE html><html>
                <head><title> 401 Unauthorized </title></head>
                <body>
                <h1>401 Unauthorized</h1>
                <p>This is a private area.</p>
                </body></html>
            """
    else:
        try:
            fin = open("./web_src" + path, "rb")
            response = _makeResponseHeader("200 OK", path) + fin.read()
            fin.close()
        except FileNotFoundError:
            response = _makeResponseHeader("404 Not Found") + b"""
                <!DOCTYPE html><html>
                <head><title> 404 Not Found </title></head>
                <body>
                <p>The requested file cannot be found.</p>
                </body></html>
                """ 
    
    conn.sendall(response)