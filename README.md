
# SMC + Telegram + cTrader AI Trading Bot

This project is a fully automated Smart Money Concept (SMC) trading bot that:
- ✅ Detects A+ SMC setups from price data
- 📩 Sends trade alerts via Telegram
- 🤖 Executes trades using the cTrader Open API
- 🐧 Fully compatible with Linux (no MetaTrader needed)

---

## 🧰 Features

- A+ setup detection based on:
  - Break of Structure (BOS)
  - Liquidity sweep
  - Fair Value Gap (FVG)
  - Order Block
- REST API trading via Spotware/cTrader
- Telegram alerts for every trade setup
- Configurable `config.json` for easy setup

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/smc_ctrader_telegram_bot.git
cd smc_ctrader_telegram_bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Fill in your credentials

Open `config.json` and set:

```json
{
  "symbol": "EURUSD",
  "risk_ratio": 2,
  "units": 10000,
  "telegram_token": "YOUR_TELEGRAM_BOT_TOKEN",
  "chat_id": "YOUR_TELEGRAM_CHAT_ID",
  "client_id": "YOUR_CTRADER_CLIENT_ID",
  "client_secret": "YOUR_CTRADER_CLIENT_SECRET",
  "refresh_token": "YOUR_CTRADER_REFRESH_TOKEN",
  "account_id": "YOUR_CTRADER_ACCOUNT_ID"
}
```

### 4. Run the bot

```bash
python smc_ctrader_bot.py
```

---

## 🔐 How to Get Credentials

### Telegram
- Create a bot via [@BotFather](https://t.me/botfather)
- Get your `chat_id` via [@userinfobot](https://t.me/userinfobot)

### cTrader
- Sign up at [Spotware Connect](https://connect.spotware.com/)
- Create an app → Get client ID & secret
- Use OAuth to get your refresh token

---

## 📄 Files

- `smc_ctrader_bot.py` — Main trading loop
- `ctrader_auth.py` — OAuth access token refresher
- `config.json` — Secure config file
- `requirements.txt` — Python dependencies

---

## 📬 Support

Feel free to reach out or open issues for questions and improvements.
