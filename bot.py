import telebot
from yt_dlp import YoutubeDL
import os

# التوكن الخاص بك
API_TOKEN = '8129938298:AAEC2a-d6baYFWnPTyrnKvcsCeYDKSmcNJk'
bot = telebot.TeleBot(API_TOKEN, threaded=True)

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "instagram.com", "facebook.com", "youtube.com"]):
        bot.reply_to(message, "🚀 جاري التحميل لمتابعين علي أصل... انتظر لحظة")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
                'quiet': True,
                'no_warnings': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                # رفع مدة الانتظار لضمان إرسال الفيديوهات الكبيرة
                bot.send_video(message.chat.id, video, timeout=300)
            
            os.remove('video.mp4')
        except Exception:
            bot.reply_to(message, "❌ حدث خطأ، يرجى المحاولة مرة أخرى لاحقاً.")
    else:
        bot.reply_to(message, "أهلاً بك! أرسل رابط فيديو من تيك توك أو يوتيوب لتحميله.")

if __name__ == "__main__":
    bot.infinity_polling()
