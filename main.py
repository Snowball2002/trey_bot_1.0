def get_stock_info(json_data):

    stocksymbol = json_data['Global Quote']['01. symbol']
    price = float(json_data['Global Quote']['05. price'])
    previous_close = float(json_data['Global Quote']['08. previous close'])
    high = float(json_data['Global Quote']['03. high'])
    low = float(json_data['Global Quote']['04. low'])



    shouldbuy = price > previous_close


    info_dictionary = {
        "stocksymbol": stocksymbol,
        "shouldbuy": shouldbuy,
        "price": price,
        "high": high,
        "low": low
    }


    print("Stock Symbol:", stocksymbol)
    print("Should Buy:", shouldbuy)
    print("Current Price:", price)
    print("High Price:", high)
    print("Low Price:", low)

    return info_dictionary



json_data = {
    "Global Quote": {
        "01. symbol": "IBM",
        "02. open": "140.0000",
        "03. high": "145.0000",
        "04. low": "139.5000",
        "05. price": "143.0000",
        "06. volume": "3000000",
        "07. latest trading day": "2024-05-22",
        "08. previous close": "142.0000",
        "09. change": "1.0000",
        "10. change percent": "0.7042%"
    }
}
