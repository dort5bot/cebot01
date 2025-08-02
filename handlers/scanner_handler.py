##✅ MegaBot - handlers/scanner_handler.py (güncel zaman destekli)

from telegram import Update from telegram.ext import ContextTypes from utils.scanner_utils import run_scanner_command

##Komut: /sc rsi<30 macd>0 vol>50 ts>65 4h

async def scanner_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): try: args = context.args

# Son parametre zaman dilimi mi? Değilse 1h al
    if args and args[-1].lower() in ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d", "1w"]:
        interval = args[-1].lower()
        filters = args[:-1]
    else:
        interval = "1h"
        filters = args

    if not filters:
        await update.message.reply_text("Lütfen filtre parametreleri girin. Örnek: /sc rsi<30 macd>0 vol>100 ts>60 4h")
        return

    result = run_scanner_command(filters, interval)

    if not result:
        await update.message.reply_text("Belirtilen kriterlere uyan coin bulunamadı.")
        return

    await update.message.reply_text(result)

except Exception as e:
    await update.message.reply_text(f"Hata oluştu: {e}")

