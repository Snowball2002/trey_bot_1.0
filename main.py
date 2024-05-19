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
info_dictionary =
{ "stocksymbol": stocksymbol,
        "shouldbuy": shouldbuy,
        "price": price,
        "high": high,
        "low": low
}
 
 
 
print (info_dictionary)



GetStock("ibm")