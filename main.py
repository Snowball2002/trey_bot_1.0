import requests

def GetStock(stocksymbol):
    apikKey = "I2FIH3DMPX4A1GDM"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apikKey}"
    httpHesponse = requests.get(url)

    json = httpHesponse.json()

    # TODO - create a dictiory from the json response and print it out. 
    # Things we need 
    # stocksymbol
    # shouldbuy - if the price is higher than the close price
    # price 
    # high 
    # low




GetStock("ibm")