from stock import Tickers, Fetcher, Query
from time import strftime

def test_Ticker_init1():
    t = Tickers(100, "test.txt")
    assert 100 == t.numTickers
    assert "test.txt" == t.fileName

def test_Ticker_OpenFile():
    t = Tickers(100, "test.txt")
    file = open(t.fileName,"w")
    assert file != None

def test_Fetcher_init1():
    f = Fetcher("test.txt", 300, "test.db")
    assert "test.txt" == f.inputFile
    assert 300 == f.timeLimit
    assert "test.db" == f.DBname

def test_Query_init1():
    q = Query("YI", "16:32", "stocks.db")
    assert q.ticker == "YI"
    assert q.time == "16:32"
    assert q.db_name == "stocks.db"

def test_Query_GetDetails():
    q = Query("YI", "16:32", "stocks.db")
    data = q.Get_Datails()
    assert data != None

