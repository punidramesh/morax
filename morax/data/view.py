import api, chart, os, pathlib
from halo import Halo

def printInfo(coin, C, name):
    info = fetchData(coin)
    coin = coin.lower()
    path = os.getcwd()
    p = str(pathlib.Path(__file__).parent.absolute())
    p1 = os.path.join(p,"assets")
    os.chdir(p1)
    txt = open(f"{coin}.txt", 'r')
    os.chdir(path)
    txt = txt.readlines()
    tag_coins = ["XLM"]
    tag = {"XLM" : "Memo"}
    j = -4
    i = 0
    data = [
        C[0]  + name,
        C[0]  + "-------",
        C[0]  + "Current Price" + C[1] +": " + info[0],
        C[0]  + "Wallet Amount" + C[1] +": " + info[1],
        C[0]  + "Current Worth" + C[1] +": " + info[2],
    ]
    if coin.upper() in tag_coins:
        data.append(C[0]  + "Address" + C[1] +": " + info[3][0][:26])
        data.append(C[0] + C[1] + info[3][0][26:])
        data.append(C[0]  + tag[coin.upper()] + C[1] +": " + info[3][1])
    else:
        if coin.upper() == "MANA":
            data.append(C[0]  + "Address" + C[1] +": " + info[3][:26])
            data.append(C[1] + info[3][26:])
        else:
            data.append(C[0]  + "Address" + C[1] +": " + info[3])
    for i in range(len(txt)):
        temp = txt[i].rstrip("\n")
        if "{c1}" in temp:
            temp = temp.replace("{c1}", C[0])
        if "{c2}" in temp:
            temp = temp.replace("{c2}",C[1])  
        if "{c3}" in temp:
            temp = temp.replace("{c3}",C[2]) 
        if "{c4}" in temp:
            temp = temp.replace("{c4}",C[3]) 
        if "{c5}" in temp:
            temp = temp.replace("{c5}",C[4])    
        if i >= 4 and i <= 4 + len(data) - 1:
            print(temp, end = '')
            print(data[j+i])
        else:
            print(temp)

@Halo(text='Fetching your wallet info 🧞‍♀️', spinner='dots')
def fetchData(coin):
    price = float(api.getSpotPrice(coin))
    Balance = api.getBalance(coin)
    balance = float(Balance[:len(Balance) - 4])
    address = api.getAddress(coin)
    worth = " INR " + "{:.4f}".format(price * balance)
    price = " INR " + "{:.6f}".format(price)
    return [price, Balance, worth, address]

def selectCoin(coin):
    if coin == 'BTC':
        Bitcoin()
    elif coin == 'ETH':
        Ethereum()
    elif coin == 'LTC':
        Litecoin()
    elif coin == 'XLM':
        Stellar()
    elif coin == 'MANA':
        Decentraland()

def Bitcoin():
    coin = "Bitcoin"
    C1 = "\u001b[38;5;215m"
    C2 = "\u001b[37m"
    printInfo("BTC", [C1,C2], coin)

def Ethereum():
    coin = "Ethereum"
    C1 = "\u001b[38;5;105m"
    C2 = "\u001b[37m"
    printInfo("ETH", [C1,C2], coin)

def Litecoin():
    coin = "Litecoin"
    C1 = "\u001b[38;5;246m"
    C2 = "\u001b[37m"
    printInfo("LTC", [C1,C2], coin)
    

def Stellar():
    coin = "Stellar Lumens"
    C1 = "\u001b[38;5;240m"
    C2 = "\u001b[37m"
    printInfo("XLM", [C1,C2], coin)

def Decentraland():
    coin = "Decentraland"
    C1 = "\u001b[38;5;203m"
    C2 = "\u001b[37m"
    C3 = "\u001b[38;5;222m"
    C4 = "\u001b[38;5;11m"
    C5 = "\u001b[38;5;196m"
    printInfo("MANA", [C1,C2,C3,C4,C5], coin)
