from stock import Tickers, Fetcher

if __name__ == "__main__":
    tick = Tickers(10, "tickers.txt")
    # tick.save_tickers()
    Kiel = Fetcher("tickers.txt")
    Kiel.fetch_all_data(5)