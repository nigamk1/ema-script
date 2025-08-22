# EMA5 Trading Alert Bot

A Python trading bot that monitors Nifty 50 index and sends Telegram alerts when the 5-minute candle closes fully above the 5-period EMA.

## Features

- Real-time monitoring of Nifty 50 (^NSEI) 5-minute candles
- EMA5 calculation and bullish signal detection
- Telegram notifications for trading alerts
- Designed to run 24/7 on Render cloud platform

## Setup Instructions

### 1. Get Telegram Bot Token and Chat ID

1. **Create a Telegram Bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Choose a name and username for your bot
   - Save the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID:**
   - Start a chat with your bot
   - Send any message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response (it's a number like `123456789`)

### 2. Deploy on Render

1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Push this code to your repository

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name:** `ema5-trading-bot`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`

3. **Set Environment Variables:**
   - In Render dashboard, go to your service
   - Click "Environment" tab
   - Add these variables:
     - `BOT_TOKEN`: Your Telegram bot token
     - `CHAT_ID`: Your Telegram chat ID

### 3. Verify Deployment

- Your service will be available at `https://your-app-name.onrender.com`
- Visit the URL to see "EMA5 Trading Alert Bot is running!"
- Check `/health` endpoint for service status

## Configuration

You can modify these settings in `main.py`:

- `SYMBOL`: Stock/index symbol (default: "^NSEI" for Nifty 50)
- `INTERVAL`: Candle interval (default: "5m")
- `PERIOD`: Data period (default: "1d")
- `EMA_PERIOD`: EMA period (default: 5)

## How It Works

1. Fetches real-time 5-minute data for Nifty 50
2. Calculates 5-period EMA for each candle
3. Checks if the entire candle (low price) is above EMA5
4. Sends Telegram alert for bullish signals
5. Avoids duplicate alerts for the same candle
6. Runs continuously 24/7

## Important Notes

- The bot uses completed candles (not the current forming candle)
- Alerts are sent only once per qualifying candle
- Service automatically restarts if it crashes
- Free Render accounts may have some limitations on uptime

## Troubleshooting

- Check Render logs if the service isn't working
- Verify your bot token and chat ID are correct
- Ensure your Telegram bot is not blocked
- Check that environment variables are set properly
