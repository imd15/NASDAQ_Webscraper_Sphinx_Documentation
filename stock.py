import sys, io, sqlite3, time, json
import requests as r
from time import strftime
from iex import Stock

"""
    stock.py
    ====================================
    Contains the class declarations and definitions for Tickers, Fetcher, and Query.
"""

class Tickers:
    def __init__(self, num_tickers, file_name):
        self.numTickers = num_tickers
        self.fileName = file_name

    def save_tickers(self):
         """
            Gathers the first n tickers from the given URL and outputs them to a file.
            Parameters
            ----------
            self.numTickers
                The number of tickers to output to the file.
            self.fileName
                The name of the file to output the tickers to.
        """
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
    def __init__(self, input_file):
        self.inputFile = input_file

    def fetch_all_data(self, time_lim, db_name):
        """
            Fetches the data for n seconds and outputs the information to a sqlite3 database.
            Parameters
            ----------
            self.inputFile
                The name of the file that the tickers are read from.
            self.timeLimit
                The number of seconds that the program fetch the information for.
            self.DBname
                The name of the database to insert the information to.
        """
        self.timeLimit = time_lim
        self.DBname = db_name
        # Columns = ["Time", "Ticker", "Low", "High", "Open", "Close", "Price", "Volume"]

        connection = sqlite3.connect(self.DBname)
        try:
            c = connection.cursor()
        except AssertionError as e:
            print(e)
            return
        # drop = "DROP TABLE IF EXISTS StockData"
        task = '''CREATE TABLE IF NOT EXISTS StockData (
                    Time none, 
                    Ticker none, 
                    Low float, 
                    High float, 
                    Open float, 
                    Close float, 
                    Price float, 
                    Volume float);'''
        # c.execute(drop)
        c.execute(task)

        tickerList = []
        with open(self.inputFile,'r') as info:
            for line in info:
                tickerList.append(line.strip())

        startingTime = time.time()
        endingTime = startingTime + self.timeLimit

        while time.time() < endingTime:
            strf_time = strftime("%H:%M")
            for ticker in tickerList:
                Titles = ["symbol","latestPrice", "latestVolume","close","open","low","high"]
                URL = f"https://ws-api.iextrading.com/1.0/stock/{ticker.strip()}/quote/"
                pureText = r.get(URL).text
                textToJSON = json.loads(pureText) # casts as dict
                sqlList = [strftime("%H:%M")]
                for x in Titles:
                    sqlList.append(textToJSON[x])

                task = f'''INSERT INTO StockData(Time, Ticker, Low, High, Open, Close, Price, Volume) 
                        VALUES (
                            '{sqlList[0]}',
                            '{sqlList[1]}',
                            '{sqlList[2]}',
                            '{sqlList[3]}',
                            '{sqlList[4]}',
                            '{sqlList[5]}',
                            '{sqlList[6]}',
                            '{sqlList[7]}');'''
                c.execute(task)

            # pass until the next minute hits
            while strf_time == strftime("%H:%M") and time.time() < endingTime:
                pass 

        connection.commit()
        connection.close()

class Query:
    def __init__(self, the_ticker, the_time, db_name):
        self.ticker = the_ticker
        self.time = the_time
        self.db_name = db_name

    def Get_Datails(self):
        """
            Queries the one row from the database that the given time and ticker correspond to.
            Parameters
            ----------
            self.ticker
                The ticker that will be queried in the database.
            self.time
                The time that will be queried in the database.
            self.db_name
                The database that will be queried.
        """
        DBName = self.db_name
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