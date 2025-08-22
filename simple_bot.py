import yfinance as yf
import time
import datetime
import requests
import os

# ==== SETTINGS ====
SYMBOL = "^NSEI"   # Nifty 50 index on Yahoo Finance
INTERVAL = "5m"    # 5 minute candles
PERIOD = "1d"      # Today's data
EMA_PERIOD = 5

# Telegram Bot setup (from environment variables)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def calculate_ema(prices, period):
    """Calculate EMA manually to avoid pandas dependency issues"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period  # Start with SMA
    
    for price in prices[period:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema

def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN or CHAT_ID not set in environment variables")
        return
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("Alert sent successfully")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print("Failed to send alert:", e)

def main():
    last_alert_time = None
    print(f"Starting EMA5 Trading Alert Bot at {datetime.datetime.now()}")
    print(f"Monitoring: {SYMBOL} on {INTERVAL} interval")
    
    while True:
        try:
            print(f"Fetching data at {datetime.datetime.now()}")
            
            # Fetch data using yfinance
            ticker = yf.Ticker(SYMBOL)
            data = ticker.history(interval=INTERVAL, period=PERIOD)
            
            if data.empty or len(data) < EMA_PERIOD + 1:
                print("Not enough data, waiting...")
                time.sleep(60)
                continue
            
            # Get last 20 candles for EMA calculation (more stable)
            recent_data = data.tail(20)
            close_prices = recent_data['Close'].tolist()
            
            # Calculate EMA for the last candle
            ema5 = calculate_ema(close_prices, EMA_PERIOD)
            
            if ema5 is None:
                print("Cannot calculate EMA, waiting...")
                time.sleep(60)
                continue
            
            # Get the second-to-last candle (completed candle)
            last_candle = recent_data.iloc[-2]
            low = last_candle['Low']
            close = last_candle['Close']
            candle_time = last_candle.name
            
            # Condition: full candle above EMA
            if low > ema5:
                if last_alert_time != candle_time:
                    msg = f"✅ Bullish Alert: Nifty 50 (5m) closed fully ABOVE {EMA_PERIOD}-EMA at {candle_time}\nClose={close:.2f}, EMA5={ema5:.2f}"
                    print(msg)
                    send_telegram_alert(msg)
                    last_alert_time = candle_time
                else:
                    print(f"Already alerted for candle {candle_time}")
            else:
                print(f"No bullish signal. Low={low:.2f}, EMA5={ema5:.2f} at {candle_time}")
                
        except Exception as e:
            print("Error:", e)
        
        # Wait 60 seconds before next check
        time.sleep(60)

if __name__ == "__main__":
    main()
