import yfinance as yf

def get_btc_data(start_date='2020-01-01'):
    # BTC-USD का डेटा डाउनलोड करें
    df = yf.download('BTC-USD', start=start_date)
    df.reset_index(inplace=True)
    return df