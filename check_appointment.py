#!/usr/bin/env python3
"""
Check appointment API for month changes
Sends Telegram notification when date range changes to a new month
Includes next month info based on local time UTC+9
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
import requests

API_URL = "https://api.ajendamentu.mj.gov.tl/api/vizitor/appointments/calender/3/6/2026/3/"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
STATE_FILE = ".last_state"

# UTC+9 timezone
UTC_PLUS_9 = timezone(timedelta(hours=9))

def get_current_month_info():
    """Fetch API and return current month info"""
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        dates = data.get("dates", {})
        start_date = dates.get("startDate")
        end_date = dates.get("endDate")
        
        # Extract month from start_date (format: YYYY-MM-DD)
        current_month = start_date[:7] if start_date else None
        
        return current_month, start_date, end_date
        
    except Exception as e:
        print(f"Error fetching API: {e}")
        return None, None, None

def get_month_name(year_month):
    """Convert YYYY-MM to month name"""
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    try:
        month_num = int(year_month.split("-")[1])
        return month_names.get(month_num, year_month)
    except:
        return year_month

def get_next_month_utc9():
    """Get next month based on UTC+9 time"""
    now_utc9 = datetime.now(UTC_PLUS_9)
    
    # Calculate next month
    if now_utc9.month == 12:
        next_month = 1
        next_year = now_utc9.year + 1
    else:
        next_month = now_utc9.month + 1
        next_year = now_utc9.year
    
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    
    return f"{next_year}-{next_month:02d}", month_names[next_month]

def send_notification(current_month, start_date, end_date):
    """Send notification via Telegram when month changes"""
    current_month_name = get_month_name(current_month)
    next_month_key, next_month_name = get_next_month_utc9()
    current_time = datetime.now(UTC_PLUS_9).strftime('%Y-%m-%d %H:%M:%S')
    
    message = (
        f"🎉 NEW APPOINTMENT MONTH AVAILABLE!\n\n"
        f"📅 Current Month: {current_month_name} {current_month[:4]}\n"
        f"   ({current_month})\n\n"
        f"📆 Date Range:\n"
        f"   Start: {start_date}\n"
        f"   End: {end_date}\n\n"
        f"🗓️  Next Month (UTC+9): {next_month_name}\n"
        f"   ({next_month_key})\n\n"
        f"⏰ Checked at: {current_time} (UTC+9)"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        print("✅ Telegram notification sent successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram notification: {e}")
        return False

def load_last_state():
    """Load last known state from file"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_state(current_month, start_date, end_date):
    """Save current state to file"""
    state = {
        "current_month": current_month,
        "start_date": start_date,
        "end_date": end_date,
        "last_check": datetime.now(UTC_PLUS_9).isoformat()
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def main():
    current_time = datetime.now(UTC_PLUS_9).strftime('%Y-%m-%d %H:%M:%S')
    print("🔍 Checking appointment calendar...")
    print(f"Current time (UTC+9): {current_time}")
    
    # Check environment variables
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        sys.exit(1)
    
    # Get current month info from API
    current_month, start_date, end_date = get_current_month_info()
    
    if current_month is None:
        print("❌ Could not fetch data from API")
        sys.exit(1)
    
    current_month_name = get_month_name(current_month)
    print(f"📅 API Date Range: {start_date} to {end_date}")
    print(f"🗓️  Current Month: {current_month_name} ({current_month})")
    
    # Load previous state
    last_state = load_last_state()
    
    if last_state:
        last_month = last_state.get("current_month")
        last_month_name = get_month_name(last_month) if last_month else "Unknown"
        print(f"📝 Last check month: {last_month_name} ({last_month})")
        
        # Check if month changed
        if current_month != last_month:
            print(f"🎉 MONTH CHANGED! {last_month_name} → {current_month_name}")
            send_notification(current_month, start_date, end_date)
        else:
            print(f"ℹ️ Still showing {current_month_name} (no change)")
    else:
        print("📝 First run - saving initial state")
        print(f"📊 Currently showing {current_month_name}")
        send_notification(current_month, start_date, end_date)
    
    # Save current state
    save_state(current_month, start_date, end_date)
    print("✅ State saved successfully")

if __name__ == "__main__":
    main()
