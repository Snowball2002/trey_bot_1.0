# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import pandas as pd

import numpy as np

import requests

from tqdm import tqdm

from ta.trend import SMAIndicator

from ta.momentum import RSIIndicator

from ta.volatility import BollingerBands



import pandas as pd

import requests

from datetime import datetime

import





import requests



url = "https://data.alpaca.markets/v2/stocks/bars?symbols=tsla&timeframe=1Hour&start=2024-02-15&end=2024-02-16&limit=1000&adjustment=raw&feed=sip&sort=asc"



headers= {

    "accept": "application/json",

    "APCA-API-KEY-ID": "PK6KYD7FSKKVCE10V1Y4",

    "APCA-API-SECRET-KEY": "vyWmMTohB5cVuN3WYMRTcNSuth7oXhbdzkUJsp43"

}



response = requests.get(url, headers=headers)
#need find a safe stradgey less risky to start for test
import time

class TradingBot:
    def __init__(self):
        # Initialize necessary variables and API connection
        pass

    def is_premarket_phase(self):
        # Implement logic to determine if it's the premarket phase (4:00 AM to 9:30 AM)
        current_time = time.localtime()
        if current_time.tm_hour < 4 or (current_time.tm_hour == 4 and current_time.tm_min < 0):
            return False
        elif current_time.tm_hour > 9 or (current_time.tm_hour == 9 and current_time.tm_min >= 30):
            return False
        else:
            return True

    def execute_trading_logic(self):
        # Implement  trading logic to find the best stock to trade during the premarket phase
        # This can involve analyzing market data, indicators, news, etc.
        # For example, you can use the get_asset_info method to fetch historical prices and calculate technical indicators
        opportunities = self.get_trading_opportunities()

        # Place trades based on the identified opportunities
        self.place_trades(opportunities)

    def get_trading_opportunities(self):
        # Implement  logic to identify trading opportunities
        # This can involve analyzing historical data, calculating indicators, etc.
        # For example, you can use the get_asset_info method to fetch historical prices and calculate technical indicators
        pass

    def place_trades(self, opportunities):
        # Implement your logic to place trades based on identified opportunities
        pass

# Define the interval for checking trading opportunities (in seconds)
interval = 300  # Check every 5 minutes

# Initialize TradingBot instance
trading_bot = TradingBot()

while True:
    # Check if it's premarket phase
    if trading_bot.is_premarket_phase():
        # Execute trading logic to find the best stock to trade
        trading_bot.execute_trading_logic()

    # Wait for the next interval
    time.sleep(interval)



class Alpaca:
    pass


def get_asset_info(self, df=None):

    """

    *Description:

    Grabs historical prices for assets, calculates RSI and Bollinger Bands tech signals, and returns a df with all this data for the assets meeting the buy criteria.

    Argument(s):

        • df: a df can be provided to specify which assets you'd like info for since this method is used in the Alpaca class. If no df argument is passed then tickers from get_trading_opportunities() method are used.

    """



    # Function to fetch historical price data

    def fetch_historical_data(symbol):

        Alpaca url = f"https://api.example.com/history/{symbol}"

        response = requests.get(url)

        if response.status_code == 200:

            return response.json()

        else:

            return None



    # Grab technical stock info:

    if df is None:

        all_tickers = self.all_tickers

    else:

        all_tickers = list(df["yf_ticker"])



    df_tech = []

    for symbol in tqdm(

        all_tickers,

        desc="• Grabbing technical metrics for " + str(len(all_tickers)) + " assets",

    ):

        try:

            historical_data = fetch_historical_data(symbol)

            if historical_data:

                Hist = pd.DataFrame(historical_data)



                for n in [14, 30, 50, 200]:

                    # Initialize MA Indicator

                    Hist["ma" + str(n)] = SMAIndicator(

                        close=Hist["Close"], window=n, fillna=False

                    ).sma_indicator()

                    # Initialize RSI Indicator

                    Hist["rsi" + str(n)] = RSIIndicator(

                        close=Hist["Close"], window=n

                    ).rsi()

                    # Initialize Hi BB Indicator

                    bb = BollingerBands(close=Hist["Close"], window=n, window_dev=2)

                    Hist["bbhi" + str(n)] = bb.bollinger_hband_indicator()

                    # Initialize Lo BB Indicator

                    Hist["bblo" + str(n)] = bb.bollinger_lband_indicator()



                df_tech_temp = Hist.iloc[-1:, -16:].reset_index(drop=True)

                df_tech_temp.insert(0, "Symbol", symbol)

                df_tech.append(df_tech_temp)

        except Exception as e:

            print(f"Error processing {symbol}: {e}")



    df_tech = [x for x in df_tech if not x.empty]

    if df_tech:

        df_tech = pd.concat(df_tech)



        # Define the buy criteria

        buy_criteria = (

            (df_tech[["bblo14", "bblo30", "bblo50", "bblo200"]] == 1).any(axis=1)

        ) | ((df_tech[["rsi14", "rsi30", "rsi50", "rsi200"]] <= 30).any(axis=1))



        # Filter the DataFrame

        buy_filtered_df = df_tech[buy_criteria]



        # Create a list of tickers to trade

        self.buy_tickers = list(buy_filtered_df["Symbol"])



        return buy_filtered_df

    else:

        print("No data fetched.")

        return pd.DataFrame()





#code for selling orders*



class YourClassName:

    def __init__(self):

        # Initialize necessary variables and API connection

        pass



    def sell_orders(self):

        """

        Description:

        Liquidates positions of assets currently held based on technical signals or to free up cash for purchases.

        Argument(s):

        • self.df_current_positions: Needed to inform how much of each position should be sold.

        """



        # Function to fetch historical price data

        def fetch_historical_data(symbol):

            url = f"https://api.example.com/history/{symbol}"

            response = requests.get(url)

            if response.status_code == 200:

                return response.json()

            else:

                return None



        # Get the current time in Eastern Time

        et_tz = pytz.timezone('US/Eastern')

        current_time = datetime.now(et_tz)



        # Define the sell criteria
        #import stradgey and stop loss here such as follwinig below a certain price or percentgge in an
        #alotted ammount of time
        TradeOpps = TradingOpportunities()

        df_current_positions = self.get_current_positions()

        df_current_positions_hist = TradeOpps.get_asset_info(

            df=df_current_positions[df_current_positions['yf_ticker'] != 'Cash'])


           #design on the 3/20/24
        # Sales based on technical indicator

        sell_criteria = ((df_current_positions_hist[['bbhi14', 'bbhi30', 'bbhi50', 'bbhi200']] == 1).any(axis=1)) | \

                        ((df_current_positions_hist[['rsi14', 'rsi30', 'rsi50', 'rsi200']] >= 70).any(axis=1))



        # Filter the DataFrame

        sell_filtered_df = df_current_positions_hist[sell_criteria]

        sell_filtered_df['alpaca_symbol'] = sell_filtered_df['Symbol'].str.replace('-', '')

        symbols = list(sell_filtered_df['alpaca_symbol'])



        # Determine whether to trade all symbols or only those with "-USD" in their name

        if self.is_market_open():

            eligible_symbols = symbols

        else:

            eligible_symbols = [symbol for symbol in symbols if "-USD" in symbol]



        # Submit sell orders for eligible symbols

        executed_sales = []

        for symbol in eligible_symbols:

            try:

                if symbol in symbols:  # Check if the symbol is in the sell_filtered_df

                    print("• selling " + str(symbol))

                    qty = df_current_positions[df_current_positions['asset'] == symbol]['qty'].values[0]
                   #insert circle ci here
                    # Make HTTP request to submit sell order



                    # response = requests.post('https://api.example.com/orders/sell', json={'symbol': symbol, 'qty': qty})

                    executed_sales.append([symbol, round(qty)])

            except Exception as e:

                continue



        executed_sales_df = pd.DataFrame(executed_sales, columns=['ticker', 'quantity'])

def self():



            self.sold_message = "• liquidated no positions based on the sell criteria"

        else:

            self.sold_message = f"• executed sell orders for {''.join([symbol + ', ' if i < len(eligible_symbols) - 1 else 'and ' + symbol for i, symbol in enumerate(eligible_symbols)])}based on the sell criteria"



        print(self.sold_message)



        # Check if the Cash row in df_current_positions is at least 10% of total holdings

        cash_row = df_current_positions[df_current_positions['asset'] == 'Cash']

        total_holdings = df_current_positions['market_value'].sum()

#once market stradgey usu detrmend will be able to vaulte do 3/26/24

        if cash_row['market_value'].values[0] / total_holdings < 0.1:

            # Sort the df_current_positions by profit_pct descending

            df_current_positions = df_current_positions.sort_values(by=['profit_pct'], ascending=False)



            # Sell the top 25% of performing assets evenly to make Cash 10% of the total portfolio

            top_half = df_current_positions.iloc[:len(df_current_positions) // 4]

            top_half_market_value = top_half['market_value'].sum()

            cash_needed = total_holdings * 0.1 - cash_row['market_value'].values[0]



            for index, row in top_half.iterrows():

                print("• selling " + str(row['asset']) + " for 10% portfolio cash requirement")

                amount_to_sell = int((row['market_value'] / top_half_market_value) * cash_needed)



                # If the amount_to_sell is zero or an APIError occurs, continue to the next iteration

                if amount_to_sell == 0:

                    continue



                try:

                    # Make HTTP request to submit sell order



                    # response = requests.post('https://api.example.com/orders/sell', json={'symbol': row['asset'], 'amount': amount_to_sell})

                    executed_sales.append([row['asset'], amount_to_sell])

                except Exception as e:

                    continue



            print("• Sold assets to reach 10% cash position")



        return executed_sales_df