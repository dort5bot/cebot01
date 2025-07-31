# ======================================
# ✅ MegaBot Final - main.py
# Ana bot başlatma, komut kayıtları, JobQueue görevleri
# ======================================

import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
)

# Gerekli başlatmalar
from utils.init_files import init_data_files
from keep_alive import keep_alive

# Dosya sistemini hazırla
init_data_files()

# Ortam değişkenlerini yükle
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Uygulamayı oluştur
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Handler'lar
from handlers.ap_handler import ap_command
from handlers.io_handler import io_command
from handlers.nls_handler import nls_command
from handlers.npr_handler import npr_command
from handlers.etf_handler import etf_command
from handlers.fr_handler import fr_command
from handlers.al_handler import al_command
from handlers.sat_handler import sat_command
from handlers.stop_handler import stop_command
from handlers.aktif_handler import aktif_command
from handlers.raporum_handler import raporum_command
from handlers.apikey_handler import apikey_command

# Komut kayıtları
application.add_handler(CommandHandler("ap", ap_command))
application.add_handler(CommandHandler("io", io_command))
application.add_handler(CommandHandler("nls", nls_command))
application.add_handler(CommandHandler("npr", npr_command))
application.add_handler(CommandHandler("etf", etf_command))
application.add_handler(CommandHandler("fr", fr_command))
application.add_handler(CommandHandler("al", al_command))
application.add_handler(CommandHandler("sat", sat_command))
application.add_handler(CommandHandler("stop", stop_command))
application.add_handler(CommandHandler("aktif", aktif_command))
application.add_handler(CommandHandler("raporum", raporum_command))
application.add_handler(CommandHandler("apikey", apikey_command))

# Job kayıtları (örnek)
from jobs.check_orders import schedule_order_check
from jobs.fr_scheduler import schedule_fr_check

schedule_order_check(application.job_queue)
schedule_fr_check(application.job_queue)

# Render Free uyku koruma
keep_alive()

# Botu başlat
if __name__ == "__main__":
    application.run_polling()
