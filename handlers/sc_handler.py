# handlers/sc_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.scanner import run_screener

async def sc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Komut argümanlarını al
        args = context.args

        # Ön tanımlı ayarlar
        interval = "1h"
        limit = 50

        # Kullanıcı parametrelerini ayıkla
        criteria = []
        for arg in args:
            if arg.endswith(('m', 'h', 'd', 'w')):
                interval = arg
            elif arg.isdigit():
                limit = int(arg)
            else:
                criteria.append(arg)

        if not criteria:
            await update.message.reply_text("Lütfen filtre kriterlerini girin. Örnek: `/sc rsi<35 macd>0 4h 80`", parse_mode='Markdown')
            return

        filters = " ".join(criteria)
        result = run_screener(filters, interval, limit)

        if result:
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("Eşleşen sonuç bulunamadı.")
    except Exception as e:
        await update.message.reply_text(f"Hata oluştu: {e}")
