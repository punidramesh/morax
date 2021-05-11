import requests, os, datetime, time, json, asciichartpy
from dotenv import load_dotenv
load_dotenv()
KEY = os.getenv('NOOMICS_API_KEY')

def getTime(curr):
    month = ''
    day = ''
    if curr.month <= 10:
        month = "0" + str(curr.month)
    else:
        month = str(curr.month)
    if curr.day <= 10:
        day = "0" + str(curr.day)
    else:
        day = str(curr.day)
    return [str(curr.year), month, day]

def getChartData(coin): 
    l1 = getTime(datetime.datetime.fromtimestamp(time.time() - 3600.0*24.0*7.0*4.0))
    start = l1[0] + "-" + l1[1] + "-" + l1[2]
    region = "INR"
    URL = f"https://api.nomics.com/v1/currencies/sparkline?key={KEY}&ids={coin}&start={start}T00%3A00%3A00Z&convert={region}"
    r = requests.get(url=URL).json()
    prices = [float(i) for i in r[0]['prices']]
    config = {
        'height' : 14,
        'colors' : [
            asciichartpy.blue,
            asciichartpy.green,
            asciichartpy.default, 
        ]
    }
    print(asciichartpy.plot( prices,
        cfg=config
        )
    )
getChartData('ETH')