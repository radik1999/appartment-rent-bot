from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder
from telegram_bot.handlers import start_handler, lend_handler, rent_handler


class Command(BaseCommand):
    help = "Starts telegram bot"

    def handle(self, *args, **kwargs):
        token = settings.TELEGRAM_BOT_TOKEN
        application = ApplicationBuilder().token(token).build()
        application.add_handler(start_handler)
        application.add_handler(lend_handler)
        application.add_handler(rent_handler)
        application.run_polling()
