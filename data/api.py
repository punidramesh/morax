import requests, os, json, random, string, sys
from binance.client import Client
from dotenv import load_dotenv
load_dotenv()
import asciichartpy

s = requests.session()
tag_coins = ["XLM","XRP"]

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
		if coin == key:
			URI = URI + str(value)
			data = s.get(URI, 
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
						'CB-VERSION':"2017-12-09"
				}).json()
			return data["data"]["balance"]["amount"] + " " + key

def getAddress(coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	for key, value in accountID.items():
		if(coin == key):
			URI = URI + str(value) + "/addresses"
			data = s.get(URI, 
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
						'CB-VERSION':"2017-12-09"
				}).json()
			if coin in tag_coins:
				address = data["data"][0]['address']
				memo = address[-10:]
				address = address[:len(address) - 19]
				return [address, memo]
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
			if coin in tag_coins:
				address = data["data"][0]['address']
				memo = address[-10:]
				address = address[:len(address) - 19]
				return [address, memo]
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

def sendMoneyWithTag(receiver_addr,tag, amount, coin):
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
			return data
			return "Sent " + data["data"]["amount"]["amount"][1:] 
			+ " to " + receiver_addr 

def getSpotPrice(coin):
	
	if coin == "XRP":
		client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
		tickers = client.get_avg_price(symbol='XRPUSDT')
		usdt = float(getSpotPrice('USDT'))
		return float(tickers['price'])*usdt

	currency = coin+"-INR"
	URI = f"https://api.coinbase.com/v2/prices/{currency}/spot"
	data = s.get(URI, 
		headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'), 
				'CB-VERSION':"2017-12-09"
		}).json()
	keys = data.keys()
	if "data" in keys:
		return data['data']['amount']
	else:
		return "Data unavailable"

def getRSI(coin):
	price = []
	client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
	klines = client.get_historical_klines(f"{coin}USDT", Client.KLINE_INTERVAL_30MINUTE, "11 May, 2021", "12 May, 2021")
	usdt = float(getSpotPrice('USDT'))
	for i in klines:
		price.append(float(i[1])*usdt)
	config = {
		'height' : 14,
		'colors' : [
			asciichartpy.blue,
			asciichartpy.green,
			asciichartpy.default, 
		]
	}
	print(asciichartpy.plot(price,
		cfg=config
		)
	)

print(sendMoneyWithTag("rw2ciyaNshpHe7bCHo4bRWq6pqqynnWKQg", 
					"2280943035",
					"0.001",
					"XRP"
))