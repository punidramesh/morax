from flask import Flask, request, render_template, redirect
import pathlib, yaml
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

#default route
@app.route('/')
def hello():
	return render_template('running.html')

#OAuth redirect route from server
@app.route('/auth/redirect')
def getResponse():
	code = request.args.get("code")
	at = None
	config = loadConfig()
	REDIRECT_URL = config.get('REDIRECT_URL')
	clientID = config.get('CLIENTID')
	secret = config.get('CLIENT_SECRET')
	STATE = config.get('STATE')

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
			config = loadConfig()

			if config["ACCESS_TOKEN"] != None or config["REFRESH_TOKEN"] != None or config["TIME"] != None:
				click.secho("Login successful ✅", fg = "green")
			else:
				click.secho("Unable to save credentials", fg = "red")
			return render_template('complete.html')
		else:
			return render_template('error.html')
	finally:
		time.sleep(3)
		shutdown_server()

def saveInfo(access_token, refresh_token):
	config = loadConfig()
	config['TIME'] = str(time.time())
	config['ACCESS_TOKEN'] = access_token
	config['REFRESH_TOKEN'] = refresh_token
	config['LOGIN_STATE'] = True

	path = os.getcwd()
	p = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
	os.chdir(p)
	with open('config.yaml','w') as yamlfile:
		yaml.safe_dump(config, yamlfile) 
		os.chdir(path)

def renewAccessToken():
	config = loadConfig()
	secret = config.get('CLIENT_SECRET')
	clientID = config.get('CLIENTID')
	REFRESH_TOKEN = config.get('REFRESH_TOKEN')
	REFRESH_URI = f"https://api.coinbase.com/oauth/token?grant_type=refresh_token&client_id={clientID}&client_secret={secret}&refresh_token={REFRESH_TOKEN}"
	try:	
		at = requests.post(REFRESH_URI).json()
		accessToken = at['access_token']
		refreshToken = at['refresh_token']
	except Exception as err:
		click.echo("Error : Unable to fetch access token, please login again")
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

def loadConfig():
	path = os.getcwd()
	p = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
	os.chdir(p)
	with open("config.yaml", "r") as f:
		os.chdir(path)
		return yaml.safe_load(f)

if __name__ == '__main__':
	app.run(port=6660)