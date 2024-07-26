from flask import Flask, request, render_template_string
import requests
import json
from pymongo import MongoClient


app = Flask(__name__)
uri = "mongodb+srv://paololaur42:2202@cluster0.mrifqgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

mycol = client["cluster0"]["stocks"] #colle



def get_stock_info(stocksymbol):
    apiKey = "W4M5Z9F1QRGCA3UX"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apiKey}"
    httpresponse = requests.get(url)
    data = httpresponse.json()




    print("API Response:", data)


    if "Global Quote" not in data:
        return {"error": "Stock symbol not found or API limit reached."}


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
            .styled-input {
                display: inline-block;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: 1px solid #007bff;
                margin: 10px; /* Space between input and button */
            }
        </style>
        <h1>This is Paolo and Luke's home page</h1>
        <form action="/stocks" method="get">
            <input type="text" name="symbol" placeholder="Enter stock symbol" class="styled-input" required>
            <button type="submit" class="styled-button">Get Stock Info</button>
        </form>
    '''


@app.route('/stocks')
def stocks():
    symbol = request.args.get('symbol')
    if not symbol:
        return "<h1>Error: No stock symbol provided</h1>"


    stock_info = get_stock_info(symbol)
    if "error" in stock_info:
        return f"<h1>Error: {stock_info['error']}</h1>"
   # Save stock info to MongoDB
    mycol.insert_one(stock_info) 

    return f'''
        <style>
            body {{
                background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee); /* Sunset gradient */
                font-family: Arial, sans-serif; /* Modern font */
                color: #ffffff; /* White text color for contrast */
                text-align: center; /* Center align text and buttons */
                padding: 50px; /* Padding around the content */
            }}
            .styled-button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: black;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.3s;
                margin: 10px;
            }}
            .styled-button:hover {{
                background-color: #0056b3;
            }}
            .stock-info {{
                text-align: left; /* Left align stock information *
                display: inline-block; /* Align to left but keep centered in parent *
                margin: 20px auto; /* Center it horizontally *
                border: 1px solid #ddd; /* Light border around the stock info *
                padding: 20px; /* Padding inside the stock info box *
                border-radius: 10px; /* Rounded corners *
                background-color: #f9f9f9; /* Light background color for stock info *
                color: #000000 * black txt for stock info *
            }}
        </style>
        <h1>Stock Information for {symbol.upper()}</h1>
        <div class="stock-info">
            <p><strong>Symbol:</strong> {stock_info['stocksymbol']}</p>
            <p><strong>Price:</strong> {stock_info['price']}</p>
            <p><strong>High:</strong> {stock_info['high']}</p>
            <p><strong>Low:</strong> {stock_info['low']}</p>
            <p><strong>Previous Close:</strong> {stock_info['previous_close']}</p>
            <p><strong>Should Buy:</strong> {'Yes' if stock_info['shouldbuy'] else 'No'}</p>
        </div>
        <a href="/" class="styled-button">Go back home</a>
        <a href="/charts" class="styled-button">View Charts</a>
    '''
@app.route('/charts')
def charts():
   symbol = request.args.get('symbol', 'IBM')


   # Get historical data for the symbol i request and make an api request for the daily chart in alpha vantage just like what we did for /stocks page 
   apiKey = "W4M5Z9F1QRGCA3UX"
   url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apiKey}"
   httpresponse = requests.get(url)
   data = httpresponse.json()


   if "Time Series (Daily)" not in data:
       return "<h1>Error: Unable to fetch historical data for the stock symbol.</h1>"


   # this shows where i get my data for the daily charts
   time_series = data["Time Series (Daily)"]
   chart_data = [
       {
           "t": date,
           "o": float(values["1. open"]),
           "h": float(values["2. high"]),
           "l": float(values["3. low"]),
           "c": float(values["4. close"])
       }
       for date, values in time_series.items()
   ]
   chart_data_json = json.dumps(chart_data)


   return render_template_string('''
       <!DOCTYPE html>
       <html>
       <head>
           <style>
               body {
                   background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                   font-family: Arial, sans-serif;
                   color: #333333;
                   text-align: center;
                   padding: 50px;
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
                   margin: 10px;
               }
               .styled-button:hover {
                   background-color: #0056b3;
               }
               .chart-container {
                   position: relative;
                   margin: auto;
                   height: 500px;
                   width: 90%;
                   max-width: 800px;
               }
           </style>
           
           <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-financial"></script>            #  supports the daily chart 
       </head>
       <body>
           <h1>{{ symbol.upper() }} Stock Chart</h1>
           <div class="chart-container">
               <canvas id="stockChart"></canvas>
           </div>
           <a href="/" class="styled-button">Go back home</a>
           <a href="/stocks" class="styled-button">Go to Stocks Info</a>
           <script>
               var ctx = document.getElementById('stockChart').getContext('2d');
               var stockChart = new Chart(ctx, {
                   type: 'candlestick',                          # candle stick style chart to make it more eradable
                   data: {
                       datasets: [{
                           label: '{{ symbol.upper() }} Stock Price',
                           data: {{ chart_data|tojson }},
                           borderColor: 'rgba(75, 192, 192, 1)',
                           backgroundColor: 'rgba(75, 192, 192, 0.2)',
                           borderWidth: 1
                       }]
                   },
                   options: {
                       responsive: true,
                       scales: {
                           x: {
                               title: {
                                   display: true,
                                   text: 'Date',
                                   color: '#000000',
                               },
                               type: 'time',
                               time: {
                                   unit: 'day',
                                   tooltipFormat: 'll'
                               },
                               grid: {
                                   display: false,
                               },
                               ticks: {
                                   maxRotation: 45,
                                   minRotation: 45,
                                   color: '#000000',
                               }
                           },
                           y: {
                               title: {
                                   display: true,
                                   text: 'Price (USD)',
                                   color: '#000000',
                               },
                               beginAtZero: false,
                               grid: {
                                   color: 'rgba(200, 200, 200, 0.3)',
                               },
                               ticks: {
                                   callback: function(value) {
                                       return '$' + value;
                                   },
                                   color: '#000000',
                               }
                           }
                       },
                       plugins: {
                           legend: {
                               display: true,
                               position: 'top',
                               labels: {
                                   color: '#000000',
                               }
                           },
                           tooltip: {
                               callbacks: {
                                   label: function(context) {
                                       var o = context.raw.o;
                                       var h = context.raw.h;
                                       var l = context.raw.l;
                                       var c = context.raw.c;
                                       return `Open: $${o}, High: $${h}, Low: $${l}, Close: $${c}`;
                                   }
                               }
                           }
                       }
                   }
               });
           </script>
       </body>
       </html>
   ''', symbol=symbol, chart_data=chart_data_json)





if __name__ == '__main__':
    app.run(debug=True)
   


#getdd info is beacasue its luke_is_the_best


#app = Flask(__name__)


#from flask import Flask


#app = Flask(__name__)


### return "Hello, World!"


   


#getdd info is beacasue its luke_is_the_best


#app = Flask(__name__)


#from flask import Flask


#app = Flask(__name__)


### return "Hello, World!"jnjkjn




