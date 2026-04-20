import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# Web Server to keep Render alive
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Telegram Bot Setup
BOT_TOKEN = '8129938298:AAEC2a-d6baYFWnPTyrnKvcsCeYDKSmcNJK'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is Active! Send me a link.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "Processing...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove('video.mp4')
        except Exception as e:
            bot.reply_to(message, "Error downloading video.")
    else:
        bot.reply_to(message, "Please send a valid link.")

# Start both Bot and Web Server
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True)
