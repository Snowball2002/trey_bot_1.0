import requests
from flask import Flask
#app.config ['server_name'=] 'luke_is_the_best:5000' #should change http /luke is the best 
app = Flask(__name__)

@app.route('/')


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
        "high": high, "low": low,
        "previous_close": previous_close
    }

    return info_dictionary

  


@app.route('/')
def index():
    stock_info = get_stock_info('IBM')
    return stock_info
#this is a diff way to do it port 5000 is the end point but the end result does not workout 
if __name__ == '__main__':
    app.run(host='Luke_is_the_best', port=5000, debug=True)
    

    get_stock_info("ibm")

#getdd info is beacasue its luke_is_the_best

#app = Flask(__name__)

#from flask import Flask

#app = Flask(__name__)

### return "Hello, World!"


