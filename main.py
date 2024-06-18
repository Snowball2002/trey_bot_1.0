import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_stock_info(stocksymbol):
    apikKey = "I2FIH3DMPX4A1GDM"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apikKey}"
    httpresponse = requests.get(url)

  
    data = httpresponse.json()

    try:
        stocksymbol = data['Global Quote']['01. symbol']
        price = float(data['Global Quote']['05. price'])
        previous_close = float(data['Global Quote']['08. previous close'])
        high = float(data['Global Quote']['03. high'])
        low = float(data['Global Quote']['04. low'])

        shouldbuy = price > previous_close
        info_dictionary = {
            "stocksymbol": stocksymbol,
            "shouldbuy": shouldbuy,
            "price": price,
            "high": high,
            "low": low,
            "previous_close": previous_close
        }
        return info_dictionary
    except KeyError as e:
      
        return {"error": f"Key error: {e}"}


@app.route('/')
def home():
    return '''
        <style>
            body {
                background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee); /* Sunset gradient */
                font-family: Arial, sans-serif; /* Modern font */
                color: #ffffff; /* White text color for contrast */
                text-align: center; /* Center align text and buttons */
                padding: 50px; /* Padding around the content */
            }
            .styled-button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s;
                margin: 10px; /* Space between buttons */
            }
            .styled-button:hover {
                background-color: #0056b3;
            }
        </style>
        <h1>This is Paolo and Luke's home page</h1>
        <a href="/stocks" class="styled-button">Stock info!</a>
    '''


@app.route('/stocks')
def index():
    stock_info = get_stock_info("IBM")
    if "error" in stock_info:
        return f"<h1>Error: {stock_info['error']}</h1>"

    return f'''
        <style>
            body {{
                font-family: Arial, sans-serif; /* Modern font */
                color: #333333; /* Dark text color */
                text-align: center; /* Center align text and buttons */
                padding: 50px; /* Padding around the content */
            }}
            .styled-button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s;
                margin: 10px; /* Space between buttons */
            }}
            .styled-button:hover {{
                background-color: #0056b3;
            }}
            .stock-info {{
                text-align: left; /* Left align stock information */
                display: inline-block; /* Align to left but keep centered in parent */
                margin: 20px auto; /* Center it horizontally */
                border: 1px solid #ddd; /* Light border around the stock info */
                padding: 20px; /* Padding inside the stock info box */
                border-radius: 10px; /* Rounded corners */
                background-color: #f9f9f9; /* Light background color for stock info */
            }}
        </style>
        <h1>Stock Information for IBM</h1>
        <div class="stock-info">
            <p><strong>Symbol:</strong> {stock_info['stocksymbol']}</p>
            <p><strong>Price:</strong> {stock_info['price']}</p>
            <p><strong>High:</strong> {stock_info['high']}</p>
            <p><strong>Low:</strong> {stock_info['low']}</p>
            <p><strong>Previous Close:</strong> {stock_info['previous_close']}</p>
            <p><strong>Should Buy:</strong> {'Yes' if stock_info['shouldbuy'] else 'No'}</p>
        </div>
        <a href="/" class="styled-button"> if you would like to go back home here idk why you would sorry :( </a>
        <a href="/charts" class="styled-button">View Charts</a>
    '''


@app.route('/charts')
def charts():
    return '''
        <style>
            body {
                background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee); /* Sunset gradient */
                font-family: Arial, sans-serif; /* Modern font */
                color: #ffffff; /* White text color for contrast */
                text-align: center; /* Center align text and buttons */
                padding: 50px; /* Padding around the content */
            }
            .styled-button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s;
                margin: 10px; /* Space between buttons */
            }
            .styled-button:hover {
                background-color: #0056b3;
            }
        </style>
        <h1>IBM Stock Charts</h1>
        <p>Their are no charts yet still learning :( </p>
        <a href="/" class="styled-button">Go back home loser</a>
        <a href="/stocks" class="styled-button"> You must go back to the Stocks Info page </a>
    '''

if __name__ == '__main__':
    app.run(debug=True)


  

#getdd info is beacasue its luke_is_the_best

#app = Flask(__name__)

#from flask import Flask

#app = Flask(__name__)

### return "Hello, World!"


