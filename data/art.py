import api
def bitcoin():
    btc = open('assets/btc.txt', 'r')
    btc = btc.readlines()
    price = float(api.getSpotPrice('BTC'))
    Balance = api.getBalance('BTC')
    balance = float(Balance[:len(Balance) - 4])
    for i in range(len(btc)):
        temp = btc[i].rstrip("\n")
        if i == 4:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:19], end = "")
            print(u"\u001b[38;5;208m" + temp[19:], end = "")
            print(u"\u001b[37m" + 3*' ' + "Bitcoin")
        elif i == 5:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;208m" + temp[17:], end = "")
            print(u"\u001b[37m" + 3*' ' + "-----------")
        elif i == 6:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;208m" + temp[17:], end = "")
            print(u"\u001b[38;5;208m" + 3*' ' + "Current Price" + u"\u001b[37m" +": INR " + str(price))
        elif i == 7:
            print(u"\u001b[38;5;208m" + temp, end = "")
            print(u"\u001b[38;5;208m" + 2*' ' + "Wallet Amount" + u"\u001b[37m" +": " + str(Balance))
        elif i == 8:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:17], end = "")
            print(u"\u001b[38;5;208m" + temp[17:], end = "")
            print(u"\u001b[38;5;208m" + 3*' ' + "Current Value" + u"\u001b[37m" +": INR " + str(price * balance))
        elif i == 9:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:20], end = "")
            print(u"\u001b[38;5;208m" + temp[20:], end = "")
            print(u"\u001b[38;5;208m" + 11*' ' + "Address" + u"\u001b[37m" +": " + api.getAddress('BTC'))
        elif i == 10:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:20], end = "")
            print(u"\u001b[38;5;208m" + temp[20:])
        elif i == 11:
            print(u"\u001b[38;5;208m" + temp[0:7], end = "")
            print(u"\u001b[37m" + temp[8:18], end = "")
            print(u"\u001b[38;5;208m" + temp[18:])
        else:
            print(u"\u001b[38;5;208m" + temp)

bitcoin()