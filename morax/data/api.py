import requests, os, json, random, string, sys, dotenv
from halo import Halo

#Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

from aiohttp import ClientSession
tag_coins = ["XLM"]
supported = ["BTC", "ETH", "LTC", "XLM", "MANA"]

def APICall(URI):
	try:
		session = requests.Session()
		response = session.get(URI,
				headers={'Authorization': "Bearer "	+ os.getenv('ACCESS_TOKEN'),
						'CB-VERSION':"2017-12-09"
				})
		return response.json()
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except Exception as err:
		print(f"An error ocurred: {err}")
	

def getAccountID():
	accountID = {}
	URI = "https://api.coinbase.com/v2/accounts"
	response_json = APICall(URI)
	keys = response_json.keys()
	if "data" in keys:
		for i in response_json["data"]:
			if len(i['id']) > 5:
				accountID[i['balance']['currency']] = i['id']
		return accountID
	else:
		print("Unable to fetch accountID")
		return ""
		

def getCoin():
	URI = "https://api.coinbase.com/v2/accounts"
	response_json = APICall(URI)
	keys = response_json.keys()
	if "data" in keys:
		for i in response_json["data"]:
			if len(i['id']) > 5:
				return i['currency']['code']
	else:
		print("Unable to determine crypto asset")

def getBalance(coin):
	if coin in supported:
		accountID = getAccountID()
		URI = "https://api.coinbase.com/v2/accounts/"
		response_json = APICall(URI)
		keys = response_json.keys()
		if "data" in keys:
			return response_json["data"][0]["balance"]["amount"] + " " + coin
		else:
			print("Unable to fetch balance")
			return ""
	print("Unsupported crypto asset")

def getAddress(coin):
	if coin in supported:
		accountID = getAccountID()
		URI = "https://api.coinbase.com/v2/accounts/"
		for key, value in accountID.items():
			if coin == key:
				URI = URI + str(value) + "/addresses"
				response_json = APICall(URI)
				keys = response_json.keys()
				if "data" in keys:
					if coin in tag_coins:
						address = response_json["data"][0]['address']
						memo = address[-10:]
						address = address[:len(address) - 19]
						return [address, memo]
					return response_json["data"][0]['address']
				else:
					print("Unable to fetch address")
					return ""
			else:
				return ""
	else:
		print("Unsupported crypto asset")

def getSpotPrice(coin):
	if coin in supported:
		exchange = coin+"-INR"
		URI = f"https://api.coinbase.com/v2/prices/{exchange}/spot"
		response_json = APICall(URI)
		keys = response_json.keys()
		if "data" in keys:
			return response_json['data']['amount']
		else:
			print("Data unavailable") 
			return ""
	else:
		print("Unsupported crypto asset")
