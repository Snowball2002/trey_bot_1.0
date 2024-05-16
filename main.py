
class StockController:
    async def GetStock(self):
        client = "HttpClient()"
        symbol = "imb"
        url = f"http://www.aphpavantage.co/query?function=global_qoutes={symbol}&apikey=demo"
        httpResponse = await client.GetAsync(url)
        response = await httpResponse.Content.ReadFromJsonAsync[StockData]()
        payload = Payload()
        payload.shouldbuy = True
        payload.stocksymbol = response.globalquote._01symbol

        payload.stockdata.high = response.globalquote._03high
        payload.stockdata.low = response.globalquote._04low
        payload.stockdata.price = response.globalquote._05price
        return Ok(response)

class Payload:
    def __init__(self):
        self.shouldbuy = None
        self.stocksymbol = None
        self.stockdata = None

class GlobalQuote:
    def __init__(self):
        self._01symbol = None
        self._02open = None
        self._03high = None
        self._04low = None
        self._05price = None
        self._06volume = None
        self._07latesttradingday = None
        self._08previousclose = None
        self._09change = None
        self._10changepercent = None

class StockData:
    def __init__(self):
        self.globalquote = GlobalQuote()

if __name__ == '__main__':
    controller = StockController()
    controller.GetStock()
