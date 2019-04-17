import sys, io, sqlite3, time
import requests as r
from time import strftime
from iex import Stock

class Tickers:
    def __init__(self, num_tickers, file_name):
        self.numTickers = num_tickers
        self.fileName = file_name

    def save_tickers(self):
        tickerList = []
        pure = r.get("https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=150").text #get pure text from the website
        i = 0 #counter
        # baseStockUrl = "https://api.iextrading.com/1.0/stock"
        for curr in pure.splitlines(): #splits lines at new line
            if i == self.numTickers:
                break
            else:
                try:
                    subst = curr[curr.rfind("symbol/")::1] # parse all lines until 'symbol/' is found https://www.nasdaq.com/symbol/asps/stock-report">
                    ticker = subst[subst.find("/")+1::1] # parse subst which contains 'asps/stock-report">'
                    ticker2 = ticker[:ticker.find("/")] #parse to just get the symbol
                    if ticker2.find("\"") == -1 and ticker2 != "":
                        outputRedirect = io.StringIO() #redirects output so it doesnt print to console
                        sys.stdout = outputRedirect #sets standard out to output redirect
                        Stock(ticker2).price() ## checks if valid ticker, if its not found go to except
                        sys.stdout = sys.__stdout__ #resets standard out back to stdout
                        i = i + 1
                        tickerList.append(ticker2)
                except:
                    pass
                    
        file = open(self.fileName,"w") #creates ticker.text to write to it.
        file.write("\n".join(tickerList)) #puts everything that was in the list created with tickers on a new line
        file.close() #closes file

class Fetcher:

    DBName = "stocks_now.db"
    Columns = ["Time", "Ticker", "Low", "High", "Open", "Close", "Price", "Volume"]

    def __init__(self, input_file):
        self.inputFile = input_file

    def fetch_all_data(self, time_lim):
        self.timeLimit = time_lim
        DBName = "stocks.db"
        # Columns = ["Time", "Ticker", "Low", "High", "Open", "Close", "Price", "Volume"]
        
        connection = sqlite3.connect(DBName)
        try:
            c = connection.cursor()
        except AssertionError as e:
            print(e)
            return

        task = '''CREATE TABLE IF NOT EXISTS StockData 
                    (Time char(5), 
                    Ticker varchar(10), 
                    Low float, 
                    High float, 
                    Open float, 
                    Close float, 
                    Price float, 
                    Volume float)'''
        c.execute(task)

        tickerList = []
        with open(self.inputFile,'r') as info:
            for line in info:
                print(line.strip())
                tickerList.append(line.strip())

        startingTime = time.time()
        endingTime = startingTime + self.timeLimit

        while time.time() < endingTime:
            strf_time = strftime("%H:%M")
            '''
                Implement logic for the getting of the stuff and shit yeh 
            '''
            
            while strf_time == strftime("%H:%M") and time.time() < endingTime:
                pass # pass until the next minute hits

        connection.commit()
        connection.close()

class Query:
    def __init__(self, the_ticker, the_time):
        self.ticker = the_ticker
        self.time = the_time

    def Get_Datails(self):
        DBName = "stocks.db"
        connection = sqlite3.connect(DBName)
        try:
            c = connection.cursor()
        except AssertionError as e:
            print(e)
            return

        task = f'''SELECT *  
                    FROM StockData 
                    WHERE Time = '{self.time}' AND Ticker = '{self.ticker}';'''
        c.execute(task)

        data = c.fetchone()
        print(data)    
            
        
        connection.commit()
        connection.close()