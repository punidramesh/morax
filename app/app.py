from flask import Flask, request, redirect
from dotenv import load_dotenv
import os, requests, json

app = Flask(__name__)
load_dotenv('.env')
REDIRECT_URL = os.getenv('REDIRECT_URL')
clientID = os.getenv('CLIENTID')
secret = os.getenv('CLIENT_SECRET')
state = os.getenv('STATE')
PORT = os.getenv('PORT')
CALLBACK_URL = os.getenv('CALLBACK_URL')
access_token = ""

@app.route('/')
def hello():
	return redirect("https://www.coinbase.com/oauth/authorize?response_type=code&client_id=7446410997bffc1c989aa8f54600a628176aede236a88d05ea55a1f0c14f059a&redirect_uri=https://localhost:5000/auth/coinbase/redirect&state=134ef5504a94&scope=wallet:user:read,wallet:accounts:read", code=302)

@app.route('/auth/coinbase/redirect')
def getResponse():
	print("Inside")
	code = request.args.get("code")
	if code != None:
		ACCESS_URI = f"https://www.coinbase.com/oauth/token?grant_type=authorization_code&code={code}&client_id={clientID}&client_secret={secret}&redirect_uri={REDIRECT_URL}"
		at = requests.post(ACCESS_URI).json()
		return at['access_token']
	else:
    		return "Invalid token"

@app.route('/auth/coinbase/callback')
def complete():
	return access_token

if __name__ == '__main__':
	app.run(ssl_context='adhoc', debug=True)