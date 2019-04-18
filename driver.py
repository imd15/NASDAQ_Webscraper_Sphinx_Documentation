"""
    Usage:
        driver.py --operation=<Ticker> [--ticker_count=<num>]
        driver.py --operation=<Fetcher> [--ticker_count=<num>] [--time_limit=<time_lim>] [--db=<dbname>]
        driver.py --operation=<Query> [--time=<time>] [--db=<dbname>] [--ticker=<ticker_name>]

    Options:
        --operation=<Ticker> Get Tickers
        --ticker_count=<num> num of tickers [default: 100]
        --time_limit=<time_lim> time limit for fetcher [default: 100]
        --db=<dbname> database name [default: "stocks.db"]

"""
import sys
import re
from stock import Tickers, Fetcher, Query
import argparse as ap
from docopt import docopt


if __name__ == "__main__":
    """
    driver.py
    ====================================
    The core module of the project. Parses the arguments and flags passed
    in and calls the corresponding functions.
    """

    #tick = Tickers(10, "tickers.txt")
    #tick.save_tickers()
    #Kiel = Fetcher("tickers.txt")
    #Kiel.fetch_all_data(5)
    #test = Query("YI","17:33")
    #test.Get_Datails()
    
    args = docopt(__doc__)
    op = sys.argv[1]
    operation = args['--operation']
    tickernum = args['--ticker_count']
    time_lim = args['--time_limit']
    curr_time = args['--time']
    ticker= args['--ticker']
    dbname= args['--db']

    #These set the default
    if tickernum == None:
        tickernum = 110
    if ticker == None:
        ticker = 'YI'
    if dbname == None:
        dbname = "stocks_new.db"
    if curr_time == None:
        curr_time = "16:32"
    if time_lim == None:
        time_lim = 120


    if operation == "Ticker":
        ticker_count =  tickernum
        #print(ticker_count)
        ticker_call = Tickers(ticker_count,"tickers.txt")
        ticker_call.save_tickers()

    elif operation == "Fetcher":
        fetcher_count =  int(tickernum)
        time_count =  int(time_lim)
        database = dbname
        # print(f"\nfetcher_count = {fetcher_count}\ntime_count = {time_count}\ndatabase = {database}\n")
        fetcher_call = Fetcher("tickers.txt")
        fetcher_call.fetch_all_data(time_count,database)
    
    elif operation == "Query":
        time_count = curr_time
        database = dbname
        
        # print(f"time_count = {time_count}\ndatabase = {database}\nticker_name = {ticker_name}")

        #print(ticker_name)
        query_call = Query(ticker,time_count,database)
        query_call.Get_Datails()