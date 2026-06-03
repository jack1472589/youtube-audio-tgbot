#!/usr/bin/env python3
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from providers import fetch_balance
from utils import parse_providers

load_dotenv()

TG_TOKEN = os.getenv('tgToken')
CHAT_ID = os.getenv('chatId')
SERVICE_PROVIDERS = os.getenv('SERVICE_PROVIDERS', '[]')
HISTORY_FILE = 'balance_history.json'

if not TG_TOKEN or not CHAT_ID:
    print("❌ Missing tgToken or chatId")
    sys.exit(1)


def load_history() -> dict:
    """Load balance history from file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_history(history: dict):
    """Save balance history to file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save history: {e}")


def get_today_key() -> str:
    """Get today's date key (YYYY-MM-DD)"""
    return datetime.now().strftime('%Y-%m-%d')


def get_yesterday_key() -> str:
    """Get yesterday's date key"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_before_yesterday_key() -> str:
    """Get day before yesterday's date key"""
    before_yesterday = datetime.now() - timedelta(days=2)
    return before_yesterday.strftime('%Y-%m-%d')


def send_message(text: str) -> bool:
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
        resp = requests.post(url, json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Send failed: {e}")
        return False


def main():
    accounts = parse_providers(SERVICE_PROVIDERS)
    
    if not accounts:
        print("❌ No accounts configured")
        return
    
    print(f"🔍 Checking {len(accounts)} account(s)...")
    
    history = load_history()
    today_key = get_today_key()
    yesterday_key = get_yesterday_key()
    before_yesterday_key = get_before_yesterday_key()
    
    messages = []
    
    for acc in accounts:
        name = acc['name']
        result = fetch_balance(acc)
        
        if result['success']:
            balance = result['balance']
            
            # Get previous balance for today
            prev_balance = None
            if name in history and today_key in history[name]:
                prev_balance = history[name][today_key].get('prev_balance')
            
            # Calculate today's consumption
            today_consumed = 0
            if prev_balance is not None:
                today_consumed = max(0, prev_balance - balance)
            
            # Store current balance
            if name not in history:
                history[name] = {}
            history[name][today_key] = {
                'balance': balance,
                'prev_balance': balance,
                'consumed': today_consumed
            }
            
            # Get consumption for yesterday and day before
            yesterday_consumed = 0
            if name in history and yesterday_key in history[name]:
                yesterday_consumed = history[name][yesterday_key].get('consumed', 0)
            
            before_yesterday_consumed = 0
            if name in history and before_yesterday_key in history[name]:
                before_yesterday_consumed = history[name][before_yesterday_key].get('consumed', 0)
            
            # Build message
            msg = f"💰 *{name}*\n"
            msg += f"余额: ${balance:.2f}\n"
            msg += f"今日消耗: ${today_consumed:.2f}\n"
            msg += f"昨日消耗: ${yesterday_consumed:.2f}\n"
            msg += f"前天消耗: ${before_yesterday_consumed:.2f}"
            
            messages.append(msg)
            print(f"✅ {name}: ${balance:.2f} (今: ${today_consumed:.2f}, 昨: ${yesterday_consumed:.2f}, 前: ${before_yesterday_consumed:.2f})")
        else:
            msg = f"❌ *{name}*: {result['error']}"
            messages.append(msg)
            print(f"❌ {name}: {result['error']}")
    
    # Save history
    save_history(history)
    
    # Send message
    if messages:
        full_msg = "\n\n".join(messages)
        if send_message(full_msg):
            print("📤 Message sent!")
        else:
            print("⚠️ Failed to send message")


if __name__ == '__main__':
    main()
