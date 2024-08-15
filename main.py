from flask import Flask, request, render_template_string
import requests
import json 
from pymongo import MongoClient
import os
import openai 
apiKey = "RE2JMDTRQVMIR6YY"
app = Flask(__name__)
uri = "mongodb+srv://paololaur42:2202@cluster0.mrifqgn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

mycol = client["cluster0"]["stocks"]

def get_stock_info(stocksymbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stocksymbol}&apikey={apiKey}"
    httpresponse = requests.get(url)
    data = httpresponse.json()

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
#live
@app.route('/')
def home():
    return '''
        <style>
            body {
                background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                font-family: Arial, sans-serif;
                color: #ffffff;
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
            .styled-input {
                display: inline-block;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                border: 1px solid #007bff;
                margin: 10px;
            }
        </style>
        <h1>Welcome to Paolo and Luke's Stock App</h1>
        <form action="/stocks" method="get">
            <input type="text" name="symbol" placeholder="Enter stock symbol" class="styled-input" required>
            <button type="submit" class="styled-button">Get Stock Info</button>
        </form>
    '''
#live
@app.route('/stocks')
def stocks():
    symbol = request.args.get('symbol')
    if not symbol:
        return "<h1>Error: No stock symbol provided</h1>"

    stock_info = get_stock_info(symbol)
    if "error" in stock_info:
        return f"<h1>Error: {stock_info['error']}</h1>"

  
    mycol.insert_one(stock_info)

    return f'''
        <style>
            body {{
                background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                font-family: Arial, sans-serif;
                color: #ffffff;
                text-align: center;
                padding: 50px;
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
                text-align: left;
                display: inline-block;
                margin: 20px auto;
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #000000;
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
        <a href="/charts?symbol={symbol}" class="styled-button">View Charts</a>
        <a href="/chat" class="styled-button">Go to Trey_bot</a>
         <a href="/heatmap" class="styled-button">View Interactive Heatmap</a>
        
    '''
#is live 
@app.route('/trey_bot')
def charts():
    symbol = request.args.get('symbol', 'IBM').upper()
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apiKey}"
    httpresponse = requests.get(url)
    data = httpresponse.json()

    if "Time Series (Daily)" not in data:
        if "Error Message" in data:
            error_message = data["Error Message"]
        elif "Note" in data:
            error_message = data["Note"]
        else:
            error_message = "Unknown error occurred."

        return f"<h1>Error: {error_message}</h1>"

    time_series = data["Time Series (Daily)"]
    chart_data = []

    # Loop the through the JSON data asked for through previous metting through chart_data as the list for such
    for date, values in time_series.items():
        chart_data.append({
            "datetime": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"])
        })

    #7 days time srious kike we spoke aout comprising the data unlike lst time:(
    chart_data.sort(key=lambda x: x["datetime"], reverse=True)
    chart_data = chart_data[:7]
    chart_data.reverse()  

    # Extract x-axis atesand y-axis closing pricesand  values for the chart like we tallked about 
    dates = [item["datetime"] for item in chart_data]
    closes = [item["close"] for item in chart_data]

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                    font-family: Arial, sans-serif;
                    color: #ffffff;
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
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>{{ symbol.upper() }} Daily Prices (Last 7 Days)</h1>
            <div class="chart-container">
                <canvas id="stockChart"></canvas>
            </div>
            <a href="/" class="styled-button">Go back home</a>
            <a href="/stocks" class="styled-button">Go to Stocks Info</a>
            <a href="/heatmap" class="styled-button">View Interactive Heatmap</a>
            <a href="/chat" class="styled-button">Go to Trey_bot</a>                      
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var ctx = document.getElementById('stockChart').getContext('2d');
                    var stockChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: {{ dates|tojson|safe }},
                            datasets: [{
                                label: '{{ symbol }} Daily Closing Prices (Last 7 Days)',
                                data: {{ closes|tojson|safe }},
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderWidth: 1,
                                fill: false
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Date',
                                        color: '#ffffff',
                                    },
                                    grid: {
                                        display: false,
                                    },
                                    ticks: {
                                        color: '#ffffff',
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Price (USD)',
                                        color: '#ffffff',
                                    },
                                    beginAtZero: false,
                                    grid: {
                                        color: 'rgba(200, 200, 200, 0.3)',
                                    },
                                    ticks: {
                                        callback: function(value) {
                                            return '$' + value;
                                        },
                                        color: '#ffffff',
                                    }
                                }
                            },
                            plugins: {
                                legend: {
                                    display: true,
                                    position: 'top',
                                    labels: {
                                        color: '#ffffff',
                                    }
                                },
                                tooltip: {
                                    callbacks: {
                                        label: function(context) {
                                            return `Price: $${context.raw}`;
                                        }
                                    }
                                }
                            }
                        }
                    });
                });
            </script>
        </body>
        </html>
    ''', symbol=symbol, dates=dates, closes=closes)
  
@app.route('/chat')
def chat():
    openai.api_key = "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"
#this would be 2 of the roles system which is you telling the bot how to act or behave 
#and user 
    messages = [
        {"role": "system",
         "content": "You're a smart assistant who is here to help people make correct and educated financial decisions when it comes to the stock market."},
        {"role": "user", "content": "Hello, how can the trey_bot help you today!"}
    ]

    try:
      #connecting to the bot and setting parameters 
        from openai import OpenAI
        client = OpenAI()
        completion = openai.ChatCompletion.create(
            model="gpt_4o_mini",  
            messages=messages,
            max_tokens=2,  
            stream=True
        )

        chat_response = ""
        for chunk in completion:
            chat_response += chunk.choices[0].delta.get('content', '')

    except Exception as e:
        chat_response = f"Error: {str(e)}"

    return render_template_string('''
           <style>
               body {
                   background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                   font-family: Arial, sans-serif;
                   color: #ffffff;
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
               .styled-input {
                   display: inline-block;
                   padding: 10px;
                   font-size: 16px;
                   border-radius: 5px;
                   border: 1px solid #007bff;
                   margin: 10px;
               }
               .chat-response {
                   text-align: left;
                   display: inline-block;
                   margin: 20px auto;
                   border: 1px solid #ddd;
                   padding: 20px;
                   border-radius: 10px;
                   background-color: #f9f9f9;
                   color: #000000;
                   width: 80%;
                   max-width: 800px;
               }
           </style>
           <h1>Chat with GPT</h1>
           <form action="/chat" method="get">
               <input type="text" name="query" placeholder="Ask something..." class="styled-input" required>
               <button type="submit" class="styled-button">Ask</button>
           </form>
           <div class="chat-response">
               <h2>Response:</h2>
               <p>{{ chat_response }}</p>
           </div>
            <a href="/" class="styled-button">Go back home</a>
            <a href="/stocks" class="styled-button">Go to Stocks Info</a>
            <a href="/heatmap" class="styled-button">View Interactive Heatmap</a>                       
       ''', chat_response=chat_response)


# Heatmap route 
 #this is a test not live yet 
@app.route('/heatmap')
def heatmap():
    SECTOR_DATA = {
        "Technology": {"change": 1.2, "stocks": ["AAPL", "MSFT", "GOOGL"],
                       "description": "Technology sector includes companies involved in the research, development and/or distribution of technologically based goods and services."},
        "Finance": {"change": -0.8, "stocks": ["JPM", "BAC", "C"],
                    "description": "Finance sector includes banks, investment funds, insurance companies, and real estate firms."},
        "Healthcare": {"change": 0.3, "stocks": ["JNJ", "PFE", "MRK"],
                       "description": "Healthcare sector includes companies that provide medical services, manufacture medical equipment or drugs, provide medical insurance, or otherwise facilitate the provision of healthcare to patients."},
        "Energy": {"change": -1.0, "stocks": ["XOM", "CVX", "COP"],
                   "description": "Energy sector includes companies engaged in the exploration, production, and distribution of energy resources."}
    }

    return f'''
           <html>
           <head>
               <style>
                   body {{
                       font-family: Arial, sans-serif;
                       background: linear-gradient(to bottom right, #ff7e5f, #feb47b, #fbc2eb, #a6c1ee);
                       text-align: center;
                       padding: 50px;
                   }}
                   .heatmap-container {{
                       display: flex;
                       flex-wrap: wrap;
                       justify-content: center;
                       gap: 20px;
                   }}
                   .sector-box {{
                       border: 1px solid #ddd;
                       border-radius: 10px;
                       padding: 20px;
                       width: 200px;
                       background-color: #f9f9f9;
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
                       margin: 10px;
                   }}
                   .styled-button:hover {{
                       background-color: #0056b3;
                   }}
               </style>
           </head>
           <body>
               <h1>Interactive Heatmap</h1>
               <div class="heatmap-container">
                   {''.join([f'<div class="sector-box"><h3>{sector}</h3><p>Change: {data["change"]}%</p><p>Stocks: {", ".join(data["stocks"])}</p><p>{data["description"]}</p></div>' for sector, data in SECTOR_DATA.items()])}
               </div>
               <a href="/" class="styled-button">Go back home</a>
               <a href="/charts" class="styled-button">View Charts</a>
               <a href="/stocks" class="styled-button">Go to Stocks Info</a>
               <a href="/chat" class="styled-button">Go to Trey_bot</a>
           </body>
           </html>
       '''
  #this is a test not live yet 


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




