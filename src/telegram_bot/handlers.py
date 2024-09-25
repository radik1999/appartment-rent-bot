from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from appartment.models import Appartment, AppartmentOwner
from telegram_bot import constants


async def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Здавати квартиру", callback_data='lend'),
            InlineKeyboardButton("Орендувати орендувати", callback_data='rent')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть варіант:", reply_markup=reply_markup)


async def lend_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Please enter appartment owner phone number")
    return 1


async def rent_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    appartments = await sync_to_async(Appartment.get_formatted_appartments)()
    for appartment in appartments:
        await query.message.reply_text(appartment)

    return ConversationHandler.END


async def ask_phone(update: Update, context: CallbackContext):
    phone_number = update.message.text

    try:
        owner = await sync_to_async(AppartmentOwner.objects.get)(phone_number=phone_number)
        context.user_data["owner"] = owner
        await update.message.reply_text(f'Welcome back {owner.first_name}!')
        await update.message.reply_text("Please enter appartment room number")
        return 3
    except AppartmentOwner.DoesNotExist:
        context.user_data["phone_number"] = phone_number
        await update.message.reply_text("Now, what is your full name?")
        return 2


async def ask_full_name(update: Update, context: CallbackContext):
    first_name, last_name = update.message.text.split()

    owner = AppartmentOwner(first_name=first_name, last_name=last_name, phone_number=context.user_data["phone_number"])
    await sync_to_async(owner.save)()

    context.user_data["owner"] = owner

    await update.message.reply_text("Please enter appartment room number")
    return 3

async def ask_room_number(update: Update, context: CallbackContext):
    context.chat_data["room_number"] = int(update.message.text)
    await update.message.reply_text("Please enter appartment cost per month in USD")
    return 4

async def ask_cost(update: Update, context: CallbackContext):
    context.chat_data["cost_per_month"] = int(update.message.text)

    await sync_to_async(Appartment.objects.get_or_create)(
        room_number=context.chat_data["room_number"],
        cost_per_month=context.chat_data["cost_per_month"],
        owner=context.user_data["owner"],
    )

    await update.message.reply_text("Your appartment was published!")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


lend_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(lend_button_handler, pattern='^lend$')],
    states={
        constants.ASK_PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        constants.ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_full_name)],
        constants.ASK_ROOM_NUMVER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_room_number)],
        constants.ASK_COST: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_cost)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

rent_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(rent_button_handler, pattern='^rent$')],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)