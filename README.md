# Appointment Monitor

This GitHub Actions workflow monitors the appointment API for March 2nd, 2026 and sends a Telegram notification when the date becomes "Quota Nakonu" (full/booked).

## Setup

### 1. Create GitHub Repository
- Create a new repository on GitHub
- Push these files to it

### 2. Add GitHub Secrets
Go to **Settings > Secrets and variables > Actions** and add:

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (from @BotFather)
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

### 3. How to Get Telegram Credentials

**Bot Token:**
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Copy the token provided

**Chat ID:**
1. Message @userinfobot on Telegram
2. It will reply with your ID
3. Copy the number (including the minus sign if it's negative)

## How It Works

- Runs every 15 minutes automatically
- Checks if March 2nd status is "Quota Nakonu"
- Uses caching to track state changes
- Sends Telegram notification ONLY when status changes from available to "Quota Nakonu"
- Won't spam you - only notifies once per status change

## Manual Trigger

You can manually trigger the workflow from the GitHub Actions tab if you want to test it.

## API Details

- **URL:** https://api.ajendamentu.mj.gov.tl/api/vizitor/appointments/calender/3/6/2026/3/
- **Monitored Date:** March 2, 2026
- **Trigger:** "Quota Nakonu" status
