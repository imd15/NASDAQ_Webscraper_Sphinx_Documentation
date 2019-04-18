"""
    stock.py
    ====================================
    Contains the class declarations and definitions for Tickers, Fetcher, and Query.
"""

import sys, io, sqlite3, time
import requests as r
from time import strftime
from iex import Stock

class Tickers:
    """
        Tickers Class pulls the Tickers from the URL that is used
        
        Parameters
        ----------
            num_tickers
                number of tickers
            file_name
                the name of the file that the Class will write to (Default = tickers.txt)
    """
    def __init__(self, num_tickers, file_name):
        """
            init function
            =============
            Parameters
            ----------
            num_tickers
                number of tickers
            file_name
                the name of the file that the Class will write to (Default = tickers.txt)
        """
        self.numTickers = num_tickers
        self.fileName = file_name

    def save_tickers(self):
        """
            save_tickers function: This function stores all the tickers and outputs it to the specified file
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
    """
    Fetcher class for stock.py this class takes all tickers, and stores the ticker info into a database
    
    Parameters
    ----------
        input_file
            the name of the file that the tickers will be read from
    """

    #DBName = "stocks_now.db"
    Columns = ["Time", "Ticker", "Low", "High", "Open", "Close", "Price", "Volume"]

    def __init__(self, input_file):
        self.inputFile = input_file

    def fetch_all_data(self, time_lim, database_name):
        """
            fetch_all_data function: fetches all of the data of tickers and stores into a specified database
            
            Parameters
            -----------
            time_lim
                the amount of time that the function is going to run for
            database_name
                the name of the database that the fetcher function is going to write to
        """
        self.timeLimit = time_lim
        DBName = database_name
        # Columns = ["Time", "Ticker", "Low", "High", "Open", "Close", "Price", "Volume"]
        
        connection = sqlite3.connect(DBName)
        try:
            c = connection.cursor()
        except AssertionError as e:
            print(e)
            return

        task = """CREATE TABLE IF NOT EXISTS StockData 
                    (Time char(5), 
                    Ticker varchar(10), 
                    Low float, 
                    High float, 
                    Open float, 
                    Close float, 
                    Price float, 
                    Volume float)"""
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
            
            while strf_time == strftime("%H:%M") and time.time() < endingTime:
                pass # pass until the next minute hits

        connection.commit()
        connection.close()

class Query:
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
    def __init__(self, the_ticker, the_time, db_name):
        self.ticker = the_ticker
        self.time = the_time
        self.db_name = db_name

    def Get_Datails(self):


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