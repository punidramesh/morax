import requests, os, json, random, string, sys
from dotenv import load_dotenv
#Testing API endpoints
s = requests.session()

def getAccountID():
	accountID = {}
	URI = "https://api.coinbase.com/v2/accounts"
	data = s.get(URI, 
		headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
				'CB-VERSION':"2017-12-09"
		}).json()
	for i in data["data"]:
		if len(i['id']) > 5:
			accountID[i['balance']['currency']] = i['id']
	return accountID

def getBalance(coin):
	accountID = getAccountID()
	balance = []
	URI = "https://api.coinbase.com/v2/accounts/"
	for key, value in accountID.items():
		if(coin == key):
			URI = URI + str(value)
			data = s.get(URI, 
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
						'CB-VERSION':"2017-12-09"
				}).json()
			return data["data"]["balance"]["amount"] + " " + key

def getAddress(coin):
	address = {}
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	for key, value in accountID.items():
		if(coin == key):
			URI = URI + str(value) + "/addresses"
			data = s.get(URI, 
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
						'CB-VERSION':"2017-12-09"
				}).json()
			return data["data"][0]['address']

def createAddress(coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	for key, value in accountID.items():
		if(coin == key):
			URI = URI + str(value) + "/addresses"
			data = s.get(URI, 
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
						'CB-VERSION':"2017-12-09"
				}).json()
			return data["data"]["address"]

def sendMoney(receiver_addr, amount, coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	idem = ''.join(random.choice(string.ascii_uppercase 
        + string.ascii_lowercase + string.digits) for _ in range(16))
	params = {
		'type':'send', 
		'to':receiver_addr,
		'amount': amount, 
		'currency': coin, 
		'idem': idem
	}
	for key, value in accountID.items():
		if(coin == key):
			data = s.post(URI, 
				headers={
				'Authorization': "Bearer "+ os.getenv('ACCESS_TOKEN'), 
				'CB-VERSION':"2017-12-09"}, 
				params = params).json()
			print("Enter Two-step verification code to continue")
			code = str(input())
			data = s.post(URI, 
			headers={'Authorization': "Bearer " + os.getenv('ACCESS_TOKEN'), 
					'CB-VERSION':"2017-12-09",
					'CB-2FA-Token': code
					}, 
			params = params).json()
			return "Sent " + data["data"]["amount"]["amount"][1:] 
			+ " to " + receiver_addr 

def requestMoney(sender_addr, amount, coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	params = {
		'type':'request', 
		'to':sender_addr,
		'amount': amount, 
		'currency': coin,
	}
	for key, value in accountID.items():
		if(coin == key):
			URI = URI + str(value) + "/transactions"
			data = s.post(URI, 
			headers={
				'Authorization': "Bearer "+ os.getenv('ACCESS_TOKEN'), 
				'CB-VERSION':"2017-12-09"}, 
			params = params).json()
			return "Request for " + data["data"]["amount"]["amount"] + " " + coin + "successful"
