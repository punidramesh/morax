import requests, os, json, random, string, sys, pathlib, yaml,click
from halo import Halo

from aiohttp import ClientSession
tag_coins = ["XLM"]
supported = ["BTC", "ETH", "LTC", "XLM", "MANA", "DOGE"]

def APICall(URI):
	try:
		config = loadConfig()
		session = requests.Session()
		response = session.get(URI,
				headers={'Authorization': "Bearer "	+ config.get('ACCESS_TOKEN'),
						'CB-VERSION':"2017-12-09"
				})
		return response.json()
	except requests.exceptions.HTTPError as http_err:
		click.echo(f"HTTP error occurred: {http_err}")
	except Exception as err:
		click.echo(f"An error ocurred: {err}")
	

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
		click.echo("Unable to fetch accountID")
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
		click.echo("Unable to determine crypto asset")

def getBalance(coin):
	if coin in supported:
		accountID = getAccountID()
		URI = "https://api.coinbase.com/v2/accounts/"
		response_json = APICall(URI)
		keys = response_json.keys()
		if "data" in keys:
			return response_json["data"][0]["balance"]["amount"] + " " + coin
		else:
			click.echo("Unable to fetch balance")
			return ""
	click.echo("Unsupported crypto asset")

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
		click.echo("Unsupported crypto asset")

def getSpotPrice(coin):
	if coin in supported:
		exchange = coin+"-INR"
		URI = f"https://api.coinbase.com/v2/prices/{exchange}/spot"
		response_json = APICall(URI)
		keys = response_json.keys()
		if "data" in keys:
			return response_json['data']['amount']
		else:
			click.echo("Data unavailable") 
			return ""
	else:
		click.echo("Unsupported crypto asset")
	
def loadConfig():
	path = os.getcwd()
	p = str(pathlib.Path(__file__).parent.absolute().parent.absolute())
	os.chdir(p)
	with open("config.yaml", "r") as f:
		os.chdir(path)
		return yaml.safe_load(f)
