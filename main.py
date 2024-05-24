import requests

def GetStock(stocksymbol):
    apikKey = "I2FIH3DMPX4A1GDM"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apikKey}"
    httpresponse = requests.get(url)

    json = httpresponse.json()

    # TODO - create a dictiory from the json response and print it out. 
    # Things we need 
    # stocksymbol
    # shouldbuy - if the price is higher than the close price
    # price 
    # high 
    # low 
    #getting a simple error preventing it from printing 
    # on line 19 @ = 
stocksymbol = json_data ['global quote'] ['01. symbol']
price = float(json_data['Global Quote']['05. price'])
previous_close = float (json_data['global quote']['0.8 previous close'])
low = float(json_data['Global Quote']['04. low'])
high = float(json_data['Global Quote']['03. high'])
info_dictionary = { "stocksymbol": stocksymbol,
        "shouldbuy": shouldbuy,
        "price": price,
        "high": high,
        "low": low
}
 
 
 
print (info_dictionary)



GetStock("ibm")