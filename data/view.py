import api, chart

def bitcoin():
    btc = open('assets/btc.txt', 'r')
    btc = btc.readlines()
    price = float(api.getSpotPrice('BTC'))
    Balance = api.getBalance('BTC')
    balance = float(Balance[:len(Balance) - 4])
    i = 0
    for i in range(len(btc)):
        temp = btc[i].rstrip("\n")
        if i == 4:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:19], end = "")
            print(u"\u001b[38;5;215m" + temp[19:], end = "")
            print(u"\u001b[38;5;215m" + 3*' ' + "Bitcoin")
        elif i == 5:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;215m" + temp[17:], end = "")
            print(u"\u001b[37m" + 3*' ' + "-----------")
        elif i == 6:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;215m" + temp[17:], end = "")
            print(u"\u001b[38;5;215m" + 3*' ' + "Current Price" + u"\u001b[37m" +": INR " + "{:.6f}".format(price))
        elif i == 7:
            print(u"\u001b[38;5;215m" + temp, end = "")
            print(u"\u001b[38;5;215m" + 2*' ' + "Wallet Amount" + u"\u001b[37m" +": " + str(Balance))
        elif i == 8:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;215m" + temp[17:], end = "")
            print(u"\u001b[38;5;215m" + 3*' ' + "Current Worth" + u"\u001b[37m" +": INR " + "{:.4f}".format(price * balance))
        elif i == 9:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:20], end = "")
            print(u"\u001b[38;5;215m" + temp[20:], end = "")
            print(u"\u001b[38;5;215m" + 11*' ' + "Address" + u"\u001b[37m" +": " + api.getAddress('BTC'))
        elif i == 10:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:20], end = "")
            print(u"\u001b[38;5;215m" + temp[20:])
        elif i == 11:
            print(u"\u001b[38;5;215m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:18], end = "")
            print(u"\u001b[38;5;215m" + temp[18:])
        else:
            print(u"\u001b[38;5;215m" + temp)
    
    print(u"\u001b[37m" + " ")
    if i == len(btc) - 1:
        chart.getChartData('BTC')

def ethereum():
    eth = open('assets/eth.txt', 'r')
    eth = eth.readlines()
    price = float(api.getSpotPrice('ETH'))
    Balance = api.getBalance('ETH')
    balance = float(Balance[:len(Balance) - 4])
    i = 0
    for i in range(len(eth)):
        temp = eth[i].rstrip("\n")
        if i == 6:
            print(u"\u001b[38;5;105m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;105m" + 9*' ' + "Ethereum")
        elif i == 7:
            print(u"\u001b[38;5;105m" + 2*" " + temp, end = "")
            print(u"\u001b[37m" + 8*' ' + "---------")
        elif i == 8:
            print(u"\u001b[38;5;105m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;105m" + 7*' ' + "Current Price" + u"\u001b[37m" +": INR " + "{:.6f}".format(price))
        elif i == 9:
            print(u"\u001b[38;5;105m"   + 2*" " + temp, end = "")
            print(u"\u001b[38;5;105m" + 6*' ' + "Wallet Amount" + u"\u001b[37m" +": " + str(Balance))
        elif i == 10:
            print(u"\u001b[38;5;105m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;105m" + 4*' ' + "Current Worth" + u"\u001b[37m" +": INR " + "{:.4f}".format(price * balance))
        elif i == 11:
            print(u"\u001b[38;5;105m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;105m" + 6*' ' + "Address" + u"\u001b[37m" +": " + api.getAddress('ETH'))
        else:
            print(u"\u001b[38;5;105m" + 2*" " + temp)
    
    print(u"\u001b[37m" + " ")
    if i == len(eth) - 1:
        chart.getChartData('ETH')

def litecoin():
    ltc = open('assets/ltc.txt', 'r')
    ltc = ltc.readlines()
    price = float(api.getSpotPrice('LTC'))
    Balance = api.getBalance('LTC')
    balance = float(Balance[:len(Balance) - 4])
    i = 0
    for i in range(len(ltc)):
        temp = ltc[i].rstrip("\n")
        if i == 4:
            print(u"\u001b[38;5;246m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;246m" + 5*' ' + "Litecoin")
        elif i == 5:
            print(u"\u001b[38;5;246m" + 2*" " + temp, end = "")
            print(u"\u001b[37m" + 5*' ' + "--------")
        elif i == 6:
            print(u"\u001b[38;5;246m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;246m" + 5*' ' + "Current Price" + u"\u001b[37m" +": INR " + "{:.6f}".format(price))
        elif i == 7:
            print(u"\u001b[38;5;246m"   + 2*" " + temp, end = "")
            print(u"\u001b[38;5;246m" + 5*' ' + "Wallet Amount" + u"\u001b[37m" +": " + str(Balance))
        elif i == 8:
            print(u"\u001b[38;5;246m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;246m" + 5*' ' + "Current Worth" + u"\u001b[37m" +": INR " + "{:.4f}".format(price * balance))
        elif i == 9:
            print(u"\u001b[38;5;246m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;246m" + 5*' ' + "Address" + u"\u001b[37m" +": " + api.getAddress('LTC'))
        else:
            print(u"\u001b[38;5;246m" + 2*" " + temp)
    
    print(u"\u001b[37m" + " ")
    if i == len(ltc) - 1:
        chart.getChartData('LTC')

def stellar():
    xlm = open('assets/xlm.txt', 'r')
    xlm = xlm.readlines()
    price = float(api.getSpotPrice('XLM'))
    Balance = api.getBalance('XLM')
    balance = float(Balance[:len(Balance) - 4])
    address = api.getAddress('XLM')
    i = 0
    for i in range(len(xlm)):
        temp = xlm[i].rstrip("\n")
        if i == 4:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Stellar Lumens")
        elif i == 5:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[37m" + 5*' ' + "--------------")
        elif i == 6:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Current Price" + u"\u001b[37m" +": INR " + "{:.6f}".format(price))
        elif i == 7:
            print(u"\u001b[38;5;240m"   + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Wallet Amount" + u"\u001b[37m" +": " + str(Balance))
        elif i == 8:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Current Worth" + u"\u001b[37m" +": INR " + "{:.4f}".format(price * balance))
        elif i == 9:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Address" + u"\u001b[37m" +": " + address[0][:26])
        elif i == 10:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(5*' ' + u"\u001b[37m" + address[0][26:])
        elif i == 11:
            print(u"\u001b[38;5;240m" + 2*" " + temp, end = "")
            print(u"\u001b[38;5;240m" + 5*' ' + "Memo" + u"\u001b[37m" +": " + address[1])
        else:
            print(u"\u001b[38;5;240m" + 2*" " + temp)
    
stellar()