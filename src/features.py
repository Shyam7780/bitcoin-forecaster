import pandas as pd
import numpy as np

def add_features(df):
    # 1. मूविंग एवरेजेज (Moving Averages)
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_14'] = df['Close'].rolling(window=14).mean()
    
    # 2. RSI (Relative Strength Index) - मोमेंटम और ओवरबॉट/ओवरसोल्ड नापने के लिए
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 3. MACD - प्राइस ट्रेंड की दिशा पकड़ने के लिए
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    
    # 4. Volatility (वोलैटिलिटी) - 7 दिन का उतार-चढ़ाव
    df['Volatility'] = df['Close'].rolling(window=7).std()
    
    # टारगेट: अगले दिन की क्लोजिंग प्राइस
    df['Target'] = df['Close'].shift(-1)
    
    # शुरुआत की खाली (NaN) वैल्यूज को हटा दें
    df.dropna(inplace=True)
    return df