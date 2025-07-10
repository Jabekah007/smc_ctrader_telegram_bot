import pandas as pd
import requests
from telegram import Bot
import time
import json
from ctrader_auth import get_access_token

with open("config.json") as f:
    config = json.load(f)

SYMBOL = config["symbol"]
RISK_RATIO = config["risk_ratio"]
UNITS = config["units"]
TELEGRAM_TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]
CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
REFRESH_TOKEN = config["refresh_token"]
ACCOUNT_ID = config["account_id"]

bot = Bot(token=TELEGRAM_TOKEN)

def detect_a_plus(df):
    df['BOS'] = df['high'] > df['high'].shift(1)
    df['LiquiditySweep'] = df['low'] < df['low'].rolling(5).min()
    df['FVG'] = df['low'].shift(1) > df['high'].shift(2)
    df['OrderBlock'] = (df['close'] < df['open']) & (df['volume'] > df['volume'].shift(1))
    df['A_Plus'] = df['BOS'] & df['LiquiditySweep'] & df['FVG'] & df['OrderBlock']
    return df

def get_candles():
    url = f"https://api.spotware.com/public/marketdata/v1/instruments/{SYMBOL}/candles"
    params = {"granularity": "M15", "count": 100}
    r = requests.get(url, params=params)
    data = r.json()['candles']
    df = pd.DataFrame([{
        "open": float(c['open']),
        "high": float(c['high']),
        "low": float(c['low']),
        "close": float(c['close']),
        "volume": float(c['volume']),
    } for c in data])
    return df

def place_trade(access_token, entry, sl, tp):
    url = f"https://api.spotware.com/accounts/{ACCOUNT_ID}/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "order": {
            "symbol": SYMBOL,
            "orderType": "MARKET",
            "side": "BUY",
            "quantity": UNITS,
            "takeProfit": {"price": round(tp, 5)},
            "stopLoss": {"price": round(sl, 5)},
        }
    }
    response = requests.post(url, json=body, headers=headers)
    return response.status_code == 201

def main():
    while True:
        df = get_candles()
        df = detect_a_plus(df)
        last = df.iloc[-1]

        if last['A_Plus']:
            entry = last['close']
            sl = last['low'] - 0.0015
            tp = entry + (entry - sl) * RISK_RATIO
            msg = (
                f"📡 A+ SMC Setup\n"
                f"Symbol: {SYMBOL}\n"
                f"Entry: {entry:.5f}\nSL: {sl:.5f}\nTP: {tp:.5f}"
            )
            bot.send_message(chat_id=CHAT_ID, text=msg)

            token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
            success = place_trade(token, entry, sl, tp)
            if success:
                bot.send_message(chat_id=CHAT_ID, text="✅ Trade Executed")
            else:
                bot.send_message(chat_id=CHAT_ID, text="❌ Trade Failed")
        else:
            print("No setup found")

        time.sleep(900)

if __name__ == "__main__":
    main()
