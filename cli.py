from dotenv import load_dotenv
import os, subprocess, pathlib, time
from webbrowser import open_new
from app.auth import renewAccessToken

load_dotenv()
login_status = os.getenv('LOGIN_STATUS')
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
BASE_URL = os.getenv('BASE_URL')

def auth():
    path = pathlib.Path().absolute()
    #start the flask server for OAuth
    subprocess.call("python3 " +  os.path.join(path,"app/auth.py") +  "&", shell=True)
    AUTH_URI = ('https://www.coinbase.com/oauth/' 
        + 'authorize?response_type=code&client_id=' + clientID + '&redirect_uri=' 
        + REDIRECT_URL + '&state=' + state
        + '&scope=wallet:user:read,wallet:accounts:read' + '&code=' + '302')
    open_new(AUTH_URI)

if login_status == 'False':
    auth()
    print("login successful")

def renewAccessToken():
    curr_time = time.time()
    refresh_time = float(os.getenv("TIME"))
    if refresh_time - curr_time == 7200.0:
        renewAccessToken()