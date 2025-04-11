import os
import time
import logging
from telegram.ext import Updater, CommandHandler
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

# Sample follower list - replace with your data fetching method
followers_data = [
    {"username": "testuser1"},
    {"username": "testuser2"},
    {"username": "testuser3"}
]

message_template = '''Are you suffering losses in binary trading… 
But just once — check this channel 🔥 It might change everything!

✅ Accurate Signals
🧠 Smart Risk Control
📈 Real Guidance

Follow me on IG: @_digital_agncy
Join VIP Now: 👉 https://t.me/Felix_deni'''

should_send = False

def start_dm(update, context):
    global should_send
    should_send = True
    update.message.reply_text("📨 DM sending started...")
    for follower in followers_data:
        if not should_send:
            update.message.reply_text("⛔ Stopped.")
            break
        try:
            cl.direct_send(message_template, [cl.user_id_from_username(follower["username"])])
            update.message.reply_text(f"✅ Sent to @{follower['username']}")
            time.sleep(60)  # delay to simulate human behavior
        except Exception as e:
            logging.error(f"Error sending to {follower['username']}: {e}")
            update.message.reply_text(f"❌ Failed to send to @{follower['username']}")
    update.message.reply_text("✅ All messages sent.")

def stop(update, context):
    global should_send
    should_send = False
    update.message.reply_text("🛑 DM sending stopped.")

def status(update, context):
    status_msg = "✅ Running..." if should_send else "⏸️ Not sending."
    update.message.reply_text(status_msg)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start_dm", start_dm))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("status", status))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
