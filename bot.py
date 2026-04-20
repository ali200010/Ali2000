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

# The NEW Token from your latest screenshot
BOT_TOKEN = '8129938298:AAFNAOIVq9NUUt fU9EN3Zpwv4dJVdU-cP-Y'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is now Active! Send me a TikTok or YouTube link.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "Processing link... please wait.")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'quiet': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("Error in download!", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Please send a valid link starting with http.")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True)
