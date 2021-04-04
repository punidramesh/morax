from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

@app.route('/')
def hello():
	return redirect("https://www.coinbase.com/oauth/authorize?response_type=code&client_id=7446410997bffc1c989aa8f54600a628176aede236a88d05ea55a1f0c14f059a&redirect_uri=https://localhost:5000/auth/coinbase/redirect&state=134ef5504a94&scope=wallet:user:read,wallet:accounts:read", code=302)

@app.route('/auth/coinbase/redirect')
def getResponse():
	return "OAuth 2.0 callback"

if __name__ == '__main__':
	app.run(ssl_context=('cert.pem', 'key.pem'))
