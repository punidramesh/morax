from flask import Flask, request, render_template, redirect
from dotenv import load_dotenv
import os, requests, json
from requests_oauthlib import OAuth2Session
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET')
load_dotenv('../.env')
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
CALLBACK_URL = os.getenv('CALLBACK_URL')
access_token = ""

@app.route('/')
def hello():
	return redirect(f"https://www.coinbase.com/oauth/authorize?response_type=code&client_id={clientID}&redirect_uri={REDIRECT_URL}&state={state}&scope=wallet:user:read,wallet:accounts:read", code=302)

@app.route('/auth/redirect')
def getResponse():
	code = request.args.get("code")
	if code != None:
		ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={REDIRECT_URL}"
		at = requests.post(ACCESS_URI).json()
		access_token = at['access_token']
		return render_template('complete.html')
	else:
			return render_template('error.html')

if __name__ == '__main__':
	app.run(port=PORT)