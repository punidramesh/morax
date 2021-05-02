from dotenv import load_dotenv
import os, subprocess, pathlib
from app.login import auth
from webbrowser import open_new

load_dotenv()
login_status = os.getenv('LOGIN_STATUS')

if login_status == 'False':
    path = pathlib.Path().absolute()
    subprocess.call("python3 " +  os.path.join(path,"app/app.py") +  "&", shell=True)
    auth()
    print("login successful")