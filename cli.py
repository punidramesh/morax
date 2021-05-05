from dotenv import load_dotenv
import os, subprocess, pathlib, time, multiprocessing
from webbrowser import open_new
from auth.auth import renewAccessToken

load_dotenv()
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
TERMINATE = os.getenv('TERMINATE')

def init():
    if os.getenv('LOGIN_STATE') == 'FALSE':
        login()
    else:
        if time.time() - float(os.getenv('TIME')) <= 7200:
            renewAccessToken()
        else:
            login()

def login():
    path = pathlib.Path().absolute()
    #start the flask server for OAuth
    subprocess.call("python3 " +  os.path.join(path,"auth/auth.py") +  "&", shell=True)
    AUTH_URI = ('https://www.coinbase.com/oauth/' 
        + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
        + REDIRECT_URL + '&state=' + state
        + '&scope=wallet:user:read,wallet:accounts:read' + '&code=' + '302')
    open_new(AUTH_URI)

init()