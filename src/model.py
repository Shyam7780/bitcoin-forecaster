import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error

def run_model(df):
    # मॉडल के लिए इनपुट्स (Features)
    features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_7', 'MA_14', 'RSI', 'MACD', 'Volatility']
    X = df[features]
    y = df['Target']
    
    # डेटा को समय के अनुसार बांटें (80% Training, 20% Testing)
    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    
    # XGBoost मॉडल सेट करें और ट्रेन करें
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    
    # टेस्टिंग डेटा पर भविष्यवाणी (Prediction) करें
    predictions = model.predict(X_test)
    
    # गलती (Error) मापें
    mape = mean_absolute_percentage_error(y_test, predictions)
    
    # ग्राफ के लिए टेस्टिंग डेट्स
    test_dates = df['Date'].iloc[split:]
    
    return predictions, y_test, mape, test_dates