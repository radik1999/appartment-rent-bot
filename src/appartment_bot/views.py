# botapp/views.py
from django.http import JsonResponse
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json


TELEGRAM_BOT_TOKEN = ''

bot = Bot(token=TELEGRAM_BOT_TOKEN)
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Handler function for /start command, showing two buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create buttons
    keyboard = [
        [InlineKeyboardButton("Button 1", callback_data='button1')],
        [InlineKeyboardButton("Button 2", callback_data='button2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with two buttons
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

# Callback function to handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle button click based on callback data
    if query.data == 'button1':
        await query.edit_message_text(text="You pressed Button 1!")
    elif query.data == 'button2':
        await query.edit_message_text(text="You pressed Button 2!")

# Django view for the webhook
async def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        update = Update.de_json(data, bot)
        await app.process_update(update)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "not allowed"}, status=405)

# Add the handlers to the application
app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button_handler))

bot.set_webhook(url='https://abcd1234.ngrok.io/webhook/')
