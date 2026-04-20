import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is Online"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# The NEW Token from your latest screenshot (11:57 AM)
BOT_TOKEN = '8129938298:AAGDQbxHy81J1mtyjV1NPWx2w-t-HuJqD5k'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Active. Send me a link to download.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "Downloading... Please wait.")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'quiet': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists('video.mp4'):
                with open('video.mp4', 'rb') as video:
                    bot.send_video(message.chat.id, video)
                os.remove('video.mp4')
            
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("Download Error!", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Please send a valid link.")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bot.polling(none_stop=True)

