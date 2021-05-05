from flask import Flask, request, render_template, redirect
import dotenv
import os, requests, subprocess, sys, time

#removes flask's init messages on CLI
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET')

#Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
STATE = os.getenv('STATE')
access_token = ""
refresh_token = ""

def saveInfo(access_token, refresh_token):
	dotenv.set_key(dotenv_file, 'TIME', str(time.time()))
	dotenv.set_key(dotenv_file, 'ACCESS_TOKEN', access_token)
	dotenv.set_key(dotenv_file, 'REFRESH_TOKEN', refresh_token)

def renewAccessToken():
	REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
	REFRESH_URI = f"https://api.coinbase.com/oauth/token?grant_type=refresh_token&client_id={clientID}&client_secret={secret}&refresh_token={REFRESH_TOKEN}"
	at = requests.post(REFRESH_URI).json()
	access_token = at['access_token']
	refresh_token = at['refresh_token']
	saveInfo()

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

#default route
@app.route('/')
def hello():
	return redirect(f"https://www.coinbase.com/oauth/authorize?response_type=code&client_id={clientID}&redirect_uri={REDIRECT_URL}&state={STATE}&scope=wallet:user:read,wallet:accounts:read", code=302)

#OAuth redirect route from server
@app.route('/auth/redirect')
def getResponse():
	code = request.args.get("code")
	try:
		if code != None:
			ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={REDIRECT_URL}"
			at = requests.post(ACCESS_URI).json()
			access_token = at['access_token']
			refresh_token = at['refresh_token']

			if access_token == '' or refresh_token == '':
				return render_template('error.html')

			saveInfo(access_token, refresh_token)
			dotenv.set_key(dotenv_file, 'LOGIN_STATE', 'TRUE')
			return render_template('complete.html')
		else:
			return render_template('error.html')
	finally:
		shutdown_server()

if __name__ == '__main__':
	app.run(port=6660)