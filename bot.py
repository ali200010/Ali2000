import telebot
import yt_dlp
import os

# Updated Token from your BotFather screenshot
BOT_TOKEN = '8129938298:AAEC2a-d6baYFWnPTyrnKvcsCeYDKSmcNJK'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a TikTok or YouTube link.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "Downloading... Please wait.")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("Error in download!", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Invalid link.")

bot.polling()

