from dotenv import load_dotenv
import os, subprocess
from app.login import auth, pid
from webbrowser import open_new
from app.app import access_token

load_dotenv('.env')
login_status = os.getenv('LOGIN_STATUS')

if login_status == 'False':
    subprocess.call("python3 /Users/prdeck/Desktop/Repo/Hades/app/app.py &", shell=True)
    auth()
    print(access_token)
    os.environ['LOGIN_STATUS'] = 'True'
    print("login successful")
    subprocess.call("kill -9 " + str(pid()), shell = True)
    