import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.environ.get("8671139635:AAEfCLWXxRj3GRdBhEVx4ThXqOtOnKrRGQg")

async def start(update: Update, context):
    await update.message.reply_text("Hello Sir, I'm Rakesh. How may I help you?")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
