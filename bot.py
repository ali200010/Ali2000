import telebot
import yt_dlp
import os

# التوكن الخاص بك الذي استخرجته من BotFather
API_TOKEN = '8129938298:AAEC2a-d6baYFWnPTyrnKvcsCeYDKSmcNJk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك يا علي! أرسل لي أي رابط فيديو من تيك توك أو يوتيوب وسأقوم بتحميله لك فوراً 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط والتحميل... انتظر لحظة")
        try:
            # إعدادات المكتبة للتحميل بأفضل جودة
            ydl_opts = {
                'outtmpl': 'video.mp4',
                'format': 'best',
                'quiet': True,
                'no_warnings': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # إرسال الفيديو للمستخدم في تلجرام
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ عذراً، حدث خطأ أثناء التحميل. تأكد من صحة الرابط.", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "يرجى إرسال رابط فيديو صحيح يحتوي على http")

# تشغيل البوت بشكل مستمر
bot.polling()

