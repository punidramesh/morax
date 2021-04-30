from dotenv import load_dotenv
import os, requests, time
from webbrowser import open_new

load_dotenv('.env')
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
BASE_URL = os.getenv('BASE_URL')
code = ''

def auth():
    AUTH_URI = ('https://www.coinbase.com/oauth/' 
        + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
        + REDIRECT_URL + '&state=' + state
        + '&scope=wallet:user:read,wallet:accounts:read' + '&code=' + '302')
    open_new(AUTH_URI)
 
def pid():
    return os.getpid()