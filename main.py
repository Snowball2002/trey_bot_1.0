import requests

def get_stock_info(stocksymbol):
    apikKey = "I2FIH3DMPX4A1GDM"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apikKey}"
    httpresponse = requests.get(url)
    
    json = httpresponse.json()

    stocksymbol = json['Global Quote']['01. symbol']
    price = json['Global Quote']['05. price']
    previous_close = json['Global Quote']['08. previous close']
    high = json['Global Quote']['03. high']
    low = json['Global Quote']['04. low']

    shouldbuy = price > previous_close

    info_dictionary = {
        "stocksymbol": stocksymbol,
        "shouldbuy": shouldbuy,
        "price": price,
        "high": high,
        "low": low, 
        "previous_close": previous_close
    }

    return ingo

get_stock_info("ibm")