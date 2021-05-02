from flask import Flask, request, render_template, redirect
from dotenv import load_dotenv
import os, requests, subprocess, sys

#removes flask's init messages on CLI
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET')

#Load env variables
load_dotenv()
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
CALLBACK_URL = os.getenv('CALLBACK_URL')
access_token = ""

#default route
@app.route('/')
def hello():
	return redirect(f"https://www.coinbase.com/oauth/authorize?response_type=code&client_id={clientID}&redirect_uri={REDIRECT_URL}&state={state}&scope=wallet:user:read,wallet:accounts:read", code=302)

#OAuth redirect route from server
@app.route('/auth/redirect')
def getResponse():
	code = request.args.get("code")
	if code != None:
		ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={REDIRECT_URL}"
		at = requests.post(ACCESS_URI).json()
		access_token = at['access_token']
		print(os.getpid())
		subprocess.call("echo ACCESS_TOKEN=" + access_token + " >> .env",shell=True)
		return render_template('complete.html')
	else:
			return render_template('error.html')

if __name__ == '__main__':
	app.run(port=PORT)