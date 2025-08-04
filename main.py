##main.py 
import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import time
import pytz

# ===============================
# ✅ Gerekli Başlatmalar
# ===============================
from utils.init_files import init_data_files
from keep_alive import keep_alive  # Sadece sunucu başlatacak, bot çalıştırmayacak

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

# Uygulama başlat
application = ApplicationBuilder().token(BOT_TOKEN).build()

# ===============================
# ✅ Komut Handler Ekleme
# ===============================
from handlers.ap_handler import get_handler as ap_handler
from handlers.io_handler import get_handler as io_handler
from handlers.nls_handler import get_handler as nls_handler
from handlers.npr_handler import get_handler as npr_handler
from handlers.etf_handler import get_handler as etf_handler
from handlers.fr_handler import get_handler as fr_handler
from handlers.al_handler import get_handler as al_handler
from handlers.sat_handler import get_handler as sat_handler
from handlers.stop_handler import get_handler as stop_handler
from handlers.aktif_handler import get_handler as aktif_handler
from handlers.raporum_handler import get_handler as raporum_handler
from handlers.apikey_handler import get_handler as apikey_handler
from handlers.p_handler import price_command, price_detailed_command
from handlers.sc_handler import sc_handler
from handlers.td_handler import register_td_handlers  # 🔥 /td komutu için eklendi


from handlers.granger_handler import granger_handler, granger_matrix_handler, matrix_handler


# 🔹 Tüm handler'ları uygulamaya kaydet
application.add_handler(ap_handler())
application.add_handler(io_handler())
application.add_handler(nls_handler())
application.add_handler(npr_handler())
application.add_handler(etf_handler())
application.add_handler(fr_handler())
application.add_handler(al_handler())
application.add_handler(sat_handler())
application.add_handler(stop_handler())
application.add_handler(aktif_handler())
application.add_handler(raporum_handler())
application.add_handler(apikey_handler())

# /p ve /pd komutları
application.add_handler(CommandHandler("p", price_command))
application.add_handler(CommandHandler("pd", price_detailed_command))

# /sc komutu
application.add_handler(CommandHandler("sc", sc_handler))

# /td komutları
register_td_handlers(application)

# Granger komutları
application.add_handler(CommandHandler("g", granger_handler))
application.add_handler(CommandHandler("GM", granger_matrix_handler))
application.add_handler(CommandHandler("m", matrix_handler))
#grandler Opsiyonel:
application.add_handler(CommandHandler("c", matrix_handler))   # Korelasyon
application.add_handler(CommandHandler("ct", matrix_handler))  # Cointegration
application.add_handler(CommandHandler("v", matrix_handler))   # VAR
application.add_handler(CommandHandler("l", matrix_handler))   # Liderlik




# ===============================
# ✅ JobQueue Görevleri
# ===============================
from jobs.check_orders import schedule_order_check
from jobs.fr_scheduler import schedule_fr_check
from jobs.etf_job import etf_daily_job

# Emir kontrol sistemi
schedule_order_check(application.job_queue)

# Fonlama oranı kontrolü
USER_ID = 123456789  # Kendi Telegram ID'inizi girin
COIN = "BTC"
schedule_fr_check(application, USER_ID, COIN)

# ETF günlük job
job_time = time(hour=6, minute=0, tzinfo=pytz.timezone("Europe/Istanbul"))
application.job_queue.run_daily(
    etf_daily_job,
    time=job_time,
    name="etf_daily_job"
)

# ===============================
# ✅ Ana Başlatıcı
# ===============================
if __name__ == "__main__":
    keep_alive()  # Sadece web sunucusunu açar
    application.run_polling()

