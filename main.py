import yfinance as yf
import pandas as pd
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
    last_alert_time = None  # track last candle time sent
    print(f"Starting EMA5 Trading Alert Bot at {datetime.datetime.now()}")
    print(f"Monitoring: {SYMBOL} on {INTERVAL} interval")
    
    # Main loop
    while True:
        try:
            # Fetch latest data
            print(f"Fetching data at {datetime.datetime.now()}")
            data = yf.download(SYMBOL, interval=INTERVAL, period=PERIOD, progress=False)

            if data.empty:
                print("No data received, retrying...")
                time.sleep(60)
                continue

            # Calculate EMA
            data["EMA5"] = data["Close"].ewm(span=EMA_PERIOD).mean()

            # Get last completed candle (use -2 to avoid incomplete current candle)
            if len(data) < 2:
                print("Not enough data, waiting...")
                time.sleep(60)
                continue
                
            last = data.iloc[-2]  # Use second last candle to ensure it's complete

            # Extract scalar values (avoids warnings)
            low = last["Low"].item()
            close = last["Close"].item()
            ema5 = last["EMA5"].item()
            candle_time = last.name  # timestamp of the candle

            # Condition: full candle above EMA
            if low > ema5:
                # Only send if it's a new candle
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

        # Wait for next check (check every minute, but only alert on new 5m candles)
        time.sleep(60)

if __name__ == "__main__":
    main()
