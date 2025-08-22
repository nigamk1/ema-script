from flask import Flask
import threading
import os
import main

app = Flask(__name__)

@app.route('/')
def hello():
    return "EMA5 Trading Alert Bot is running!"

@app.route('/health')
def health():
    return {"status": "healthy", "service": "ema5-trading-bot"}

def run_trading_bot():
    """Run the trading bot in a separate thread"""
    main.main()

if __name__ == '__main__':
    # Start the trading bot in a background thread
    bot_thread = threading.Thread(target=run_trading_bot, daemon=True)
    bot_thread.start()
    
    # Start the Flask web server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
