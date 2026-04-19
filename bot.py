import telebot
from yt_dlp import YoutubeDL
import os

# ضع التوكن الخاص بك هنا
BOT_TOKEN = '7548231015:AAH6vW8pYv9_6nS6fNId8N-x66_S5u5Yj-o'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو من تيك توك أو يوتيوب وسأقوم بتحميله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        msg = bot.reply_to(message, "⏳ جاري التحميل، انتظر قليلاً...")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'quiet': True
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ: {str(e)}", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "الرجاء إرسال رابط صحيح.")

bot.polling()


