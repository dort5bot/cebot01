##3
#nls_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.nls_utils import append_signal, check_signals

async def nls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if args:
            symbol = args[0].upper()
            success = append_signal(symbol)
            if success:
                await update.message.reply_text(f"✅ {symbol} sinyal olarak eklendi.")
            else:
                await update.message.reply_text(f"❌ {symbol} için sinyal oluşturulamadı.")
        else:
            result = check_signals()
            await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("❌ /nls komutunda hata oluştu.")
        print(f"[NLS HATA]: {e}")

def get_handler():
    return CommandHandler("nls", nls_command)
