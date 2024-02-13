from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from socketserver import BaseServer

f = open("users.json")
users = json.load(f)

routes = {
    "/": open("index.html").read(),
    "/welcome": "Hello World!",
    "/about": "copyright reserved by Blade",
    "/index": open("index.html").read(),
    "/login": open("login.html").read(),
    "/accept": open("user_home.html").read(),
    "/register": open("register.html").read(),
}
error = False
error_message = ""
class TestServer(BaseHTTPRequestHandler):
    # def is the keyword for function
    # function in Java
    # this is the entry server waiting for http GET request
    # we are writing an http get response
    def do_GET(self):
        global error
        global error_message
        self.send_response(200) # OK
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if error:
            error = False
        else:
            error_message = ""
        for route in routes:
            if route == self.path or (self.path.startswith(route) and route != '/'):
                self.wfile.write(bytes(routes[route].replace("###ERROR###", error_message), "UTF-8"))
                break
        
    def do_POST(self):
        global error
        global error_message
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        pairs = post_data.split('&')
        form = {}
        for pair in pairs:
            kvp = pair.split('=')
            form[kvp[0]] = kvp[1]
        match = False
        foundUser = False
        for key in users:
            user = users[key]
            if form["username"] == user["username"]:
                foundUser = True
            if form["username"] == user["username"] and form["password"] == user["password"]:
                match = True
                break
        if self.path == "/accept":
            if match:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(routes[self.path].replace("###USER###", form["username"]), "UTF-8"))
            else:
                error = True
                error_message = "Incorrect Username and password"
                print(error_message)
                self.send_response(301)
                self.send_header('Location','/login')
                self.end_headers()
        elif self.path == "/register":
            # same username, reject
            if foundUser:
                error = True
                error_message = "Username is already in the system."
                self.send_response(301)
                self.send_header('Location','/register')
                self.end_headers()
            # password and password2 doesn't match, reject
            elif form["password"] != form["password2"]:
                error = True
                error_message = "Passwords mismatch."
                self.send_response(301)
                self.send_header('Location','/register')
                self.end_headers()
            # store the username and password, and show the user home, accept
            else:
                error = False
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                users[str(len(users))] = {
                    "username": form["username"],
                    "password": form["password"]
                }
                with open("users.json", "w") as outfile:
                    json.dump(users, outfile)
                self.wfile.write(bytes(routes["/accept"].replace("###USER###", form["username"]), "UTF-8"))
    def redirect(self):
        self.send_response(301)
        self.send_header('Location','/login')
        self.end_headers()
        
# this is like run method
if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8080), TestServer)
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")