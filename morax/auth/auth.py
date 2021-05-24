from flask import Flask, request, render_template, redirect
import dotenv
import os, requests, subprocess, time, sys, click

#removes flask's init messages on CLI
import logging
import warnings
warnings.filterwarnings("ignore")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET')

#Load env variables
dotenv_file = dotenv.find_dotenv()

#default route
@app.route('/')
def hello():
	return render_template('running.html')

#OAuth redirect route from server
@app.route('/auth/redirect')
def getResponse():
	code = request.args.get("code")
	at = None
	dotenv.load_dotenv(dotenv_file)
	REDIRECT_URL = os.getenv('REDIRECT_URL')
	clientID = os.getenv('CLIENTID')
	secret = os.getenv('CLIENT_SECRET')
	STATE = os.getenv('STATE')

	try:
		if code != None:
			ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={REDIRECT_URL}"
		
			try:	
				at = requests.post(ACCESS_URI).json()
				access_token = at['access_token']
				refresh_token = at['refresh_token']
			except Exception as err:
				print("Error : ", err)
				return render_template('error.html')

			saveInfo(access_token, refresh_token)
			return render_template('complete.html')
		else:
			return render_template('error.html')
	finally:
		shutdown_server()

def saveInfo(access_token, refresh_token):
	dotenv.set_key(dotenv_file, 'TIME', str(time.time()))
	dotenv.set_key(dotenv_file, 'ACCESS_TOKEN', access_token)
	dotenv.set_key(dotenv_file, 'REFRESH_TOKEN', refresh_token)

def renewAccessToken():
	dotenv.load_dotenv(dotenv_file)
	secret = os.getenv('CLIENT_SECRET')
	clientID = os.getenv('CLIENTID')
	REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
	REFRESH_URI = f"https://api.coinbase.com/oauth/token?grant_type=refresh_token&client_id={clientID}&client_secret={secret}&refresh_token={REFRESH_TOKEN}"
	try:	
		at = requests.post(REFRESH_URI).json()
		accessToken = at['access_token']
		refreshToken = at['refresh_token']
	except Exception as err:
		print("Error : Unable to fetch access token, please login again")
	saveInfo(accessToken, refreshToken)

def shutdown_server():
	time.sleep(2)
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

def getScope():
	scopes = ["wallet:accounts:read", #List user’s accounts and their balances
				"wallet:addresses:read", #List account’s bitcoin or ethereum addresses
	]

	res = ""
	for i in range(len(scopes) - 1):
		res += scopes[i] + ","
	return res + scopes[len(scopes) - 1]

if __name__ == '__main__':
	app.run(port=6660)