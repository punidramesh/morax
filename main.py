import dotenv
import os, subprocess, pathlib, time, string, random, requests
from webbrowser import open_new
from auth.auth import renewAccessToken, getScope
from data import api

#Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
temp = 0

def genState():
    state = ''.join(random.choice(string.ascii_uppercase 
        + string.ascii_lowercase + string.digits) for _ in range(16))
    dotenv.set_key(dotenv_file, 'STATE', state)

def init():
    if os.getenv('LOGIN_STATE') == 'FALSE':
        login()
    else:
        if time.time() - float(os.getenv('TIME')) <= 7200:
            renewAccessToken()
        else:
            login()
    return 1

def login():
    path = pathlib.Path().absolute()
    #start the flask server for OAuth
    subprocess.call("python3 " +  os.path.join(path,"auth/auth.py") +  "&", shell=True)
    genState()
    AUTH_URI = ('https://www.coinbase.com/oauth/' 
        + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
        + REDIRECT_URL + '&state=' + os.getenv('STATE')
        + '&scope=' + getScope() + '&meta[send_limit_amount]=1'+
        '&meta[send_limit_currency]=USD'+'&code=' + '302')
    open_new(AUTH_URI)

login()