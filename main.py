import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv

# .env fayldan kalitlarni o‘qish
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI mijozini yaratish
client = OpenAI(api_key=OPENAI_KEY)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men sun’iy intellekt yordamchisiman 🤖\nSavolingizni yozing:"
    )

# Foydalanuvchi xabarlarini AI orqali javoblash
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))

print("✅ Bot ishga tushdi...")
app.run_polling()
