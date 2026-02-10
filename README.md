# Appointment Monitor

A GitHub Actions workflow that monitors the Timor-Leste government appointment API and sends Telegram notifications when new appointment months become available.

## Features

- 🔍 **Monitors API every 15 minutes** for month changes
- 🔔 **Sends Telegram notifications** only when appointment months change
- 🗓️ **Tracks dynamically** - works for any month (Feb→Mar, Mar→Apr, etc.)
- ⏰ **UTC+9 timezone support** - shows next month based on local time
- 🚀 **Runs 24/7 automatically** on GitHub Actions (free)

## How It Works

The script checks the appointment API every 15 minutes:
- Compares current month with previous state
- **Sends notification ONLY when month changes** (e.g., February → March)
- No spam - silent checks when month stays the same
- Includes date range and next month info (UTC+9)

## Setup

### 1. Prerequisites
- GitHub account
- Telegram account

### 2. Add GitHub Secrets

Go to **Settings > Secrets and variables > Actions** in your repository and add:

| Secret Name | Value |
|------------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID from @userinfobot |

### 3. Get Telegram Credentials

**Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Chat ID:**
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your ID (format: `123456789`)
3. Copy the number

### 4. Deploy

Push code to GitHub and the workflow starts automatically!

## Usage

### Automatic Monitoring
The workflow runs every 15 minutes and will notify you when:
- ✅ A new appointment month becomes available
- ✅ The API date range changes to a different month

### Manual Trigger
You can manually run the check anytime:
1. Go to **Actions** tab in your repository
2. Select "Check Appointment Status"
3. Click **Run workflow**

### First Run
- You will receive one notification showing the current month
- After that, notifications only when month changes

## API Details

- **Endpoint:** `https://api.ajendamentu.mj.gov.tl/api/vizitor/appointments/calender/3/6/2026/3/`
- **Service:** Timor-Leste government appointment system
- **Monitors:** Month changes in the appointment calendar

## Example Notification

```
🎉 NEW APPOINTMENT MONTH AVAILABLE!

📅 Current Month: March 2026
   (2026-03)

📆 Date Range:
   Start: 2026-03-02
   End: 2026-03-26

🗓️  Next Month (UTC+9): April
   (2026-04)

⏰ Checked at: 2026-02-11 14:30:00 (UTC+9)
```

## Workflow Schedule

- **Frequency:** Every 15 minutes
- **Trigger:** Cron schedule (`*/15 * * * *`)
- **Manual:** Can be triggered manually from Actions tab

## State Management

The workflow uses GitHub Actions cache to store the last known state between runs, ensuring:
- No duplicate notifications
- Persistent tracking across workflow runs
- Minimal API calls

## License

MIT License - Feel free to use and modify!

---

**Note:** This is an unofficial monitoring tool for the Timor-Leste appointment system.
