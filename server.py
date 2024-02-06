from http.server import BaseHTTPRequestHandler, HTTPServer

routes = {
    "/": "Homepage",
    "/welcome": "Hello World!",
    "/about": "copyright reserved by Blade",
    "/index": open("index.html").read(),
    "/login": open("login.html").read(),
}

class TestServer(BaseHTTPRequestHandler):
    # def is the keyword for function
    # function in Java
    # this is the entry server waiting for http GET request
    # we are writing an http get response
    def do_GET(self):
        self.send_response(200) # OK
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(routes[self.path], "UTF-8"))
        
        
        
# this is like run method
if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), TestServer)
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")