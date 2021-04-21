from dotenv import load_dotenv
import os, requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new

load_dotenv('.env')
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
CALLBACK_URL = os.getenv('CALLBACK_URL')

class HTTPServerHandler(BaseHTTPRequestHandler):

    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        AUTH_URI = ('https://www.coinbase.com/oauth/' 
            + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
            + REDIRECT_URL + '&state=' + state
            + '&scope=wallet:user:read,wallet:accounts:read' + '&code=' + '302')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if 'code' in self.path:
            print("inside code")
            code = self.path.split('=')[1]
            ACCESS_URI = 'https://www.coinbase.com/oauth/token?grant_type=authorization_code'
            + '&code=' + code + '&client_id=' + clientID + '&client_secret=' + secret + '&redirect_uri=' + CALLBACK_URL
            self.access_token = str(urlopen(ACCESS_URI).read(), 'utf-8')

class TokenHandler:
    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        AUTH_URI = ('https://www.coinbase.com/oauth/' 
            + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
            + REDIRECT_URL + '&state=' + state
            + '&scope=wallet:user:read,wallet:accounts:read' + '&code=' + '302')
        open_new(AUTH_URI)
        httpServer = HTTPServer(
                ('localhost', 5000),
                lambda request, address, server: HTTPServerHandler(
                    request, address, server, self._id, self._secret))
        httpServer.handle_request()
        print("done login")
        return httpServer.access_token 
        
    #ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={CALLBACK_URL}"
    #at = requests.post(ACCESS_URI)

tk = TokenHandler(clientID, state)
print(tk.get_access_token())