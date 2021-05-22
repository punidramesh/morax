import requests, os, json, random, string, sys, dotenv
from binance.client import Client
from halo import Halo

#Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

from aiohttp import ClientSession
tag_coins = ["XLM","XRP"]

def getAccountID():
	accountID = {}
	URI = "https://api.coinbase.com/v2/accounts"
	session = requests.Session()
	try:
		response = session.get(URI,
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
						'CB-VERSION':"2017-12-09"
				})
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		for i in response_json["data"]:
			if len(i['id']) > 5:
				accountID[i['balance']['currency']] = i['id']
		return accountID

def getCoin():
	URI = "https://api.coinbase.com/v2/accounts"
	session = requests.Session()
	try:
		response = session.get(URI,
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
						'CB-VERSION':"2017-12-09"
				})
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		for i in response_json["data"]:
			if len(i['id']) > 5:
				return i['currency']['code']

def getBalance(coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	session = requests.Session()
	try:
		for key, value in accountID.items():
			if coin == key:
				response = session.get(URI,
						headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
								'CB-VERSION':"2017-12-09"
						})
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		return response_json["data"][0]["balance"]["amount"] + " " + key

def getAddress(coin):
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	session = requests.Session()
	try:
		for key, value in accountID.items():
			if coin == key:
				URI = URI + str(value) + "/addresses"
				response = session.get(URI,
						headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
								'CB-VERSION':"2017-12-09"
						})
			else:
				return
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		if coin in tag_coins:
			address = response_json["data"][0]['address']
			memo = address[-10:]
			address = address[:len(address) - 19]
			return [address, memo]
		return response_json["data"][0]['address']

@Halo(text='Fetching your new address from Coinbase 🧞‍♀️', spinner='dots')
def createAddress(coin):	
	accountID = getAccountID()
	URI = "https://api.coinbase.com/v2/accounts/"
	session = requests.Session()
	try:
		for key, value in accountID.items():
			if coin == key:
				URI = URI + str(value) + "/addresses"
				response = session.get(URI,
						headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
								'CB-VERSION':"2017-12-09"
						})
			else:
				return
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		if coin in tag_coins:
			address = response_json["data"][0]['address']
			memo = address[-10:]
			address = address[:len(address) - 19]
			return [address, memo]
		return response_json["data"][0]["address"]

def getSpotPrice(coin):
	try:
		session = requests.Session()
		if coin == "XRP":
			client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
			tickers = client.get_avg_price(symbol='XRPUSDT')
			usdt = float(getSpotPrice('USDT'))
			return float(tickers['price'])*usdt

		currency = coin+"-INR"
		URI = f"https://api.coinbase.com/v2/prices/{currency}/spot"
		response = session.get(URI,
			headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
					'CB-VERSION':"2017-12-09"
			})
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	finally:
		response_json = response.json()
		keys = response_json.keys()
		if "data" in keys:
			return response_json['data']['amount']
		else:
			return "Data unavailable"
