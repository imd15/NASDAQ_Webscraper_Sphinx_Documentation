import sys
import re
from stock import Tickers, Fetcher, Query
import argparse as ap

if __name__ == "__main__":
    #tick = Tickers(10, "tickers.txt")
    #tick.save_tickers()
    #Kiel = Fetcher("tickers.txt")
    #Kiel.fetch_all_data(5)
    #test = Query("YI","17:33")
    #test.Get_Datails()

   

    op = sys.argv[1]
    operation = (sys.argv[1]).split("=")[1]

    if operation == "Ticker":
        ticker_count =  int((sys.argv[2]).split("=")[1])
        #print(ticker_count)
        ticker_call = Tickers(ticker_count,"tickers.txt")

        ticker_call.save_tickers()

    elif operation == "Fetcher":
        fetcher_count =  (sys.argv[2]).split("=")[1]
        time_count =  int((sys.argv[3]).split("=")[1])
        database = (sys.argv[4]).split("=")[1]
        print(fetcher_count, time_count, database)
        fetcher_call = Fetcher("tickers.txt")
        fetcher_call.fetch_all_data(time_count,database)
    
    elif operation == "Query":
        time_count = (sys.argv[2]).split("=")[1]
        database = (sys.argv[3]).split("=")[1]
        ticker_name = re.sub("'",'', (sys.argv[4]).split("=")[1])

        #print(ticker_name)
        query_call = Query(ticker_name,time_count,database)
        query_call.Get_Datails()