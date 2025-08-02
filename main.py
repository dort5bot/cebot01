# 📁 main.py
import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from datetime import time
import pytz

# ===============================
# ✅ Gerekli Başlatmalar
# ===============================
from utils.init_files import init_data_files
from keep_alive import keep_alive

# Dosya sistemini hazırla
init_data_files()

# Ortam değişkenlerini yükle (.env içinden)
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

application.add_handler(ap_handler())
application.add_handler(io_handler())
application.add_handler(nls_handler())
application.add_handler(npr_handler())
application.add_handler(etf_handler())  # ✅ ETF entegresi
application.add_handler(fr_handler())
application.add_handler(al_handler())
application.add_handler(sat_handler())
application.add_handler(stop_handler())
application.add_handler(aktif_handler())
application.add_handler(raporum_handler())
application.add_handler(apikey_handler())

# ===============================
# ✅ JobQueue Görevleri
# ===============================
from jobs.check_orders import schedule_order_check
from jobs.fr_scheduler import schedule_fr_check
from jobs.etf_job import etf_daily_job

# Emir kontrol sistemini başlat
schedule_order_check(application.job_queue)

# FR görev örneği (kullanıcı özelinde)
USER_ID = 123456789  # ⚠️ Kendi ID'inizle değiştirin
COIN = "BTC"         # ⚠️ İzlenen coin
schedule_fr_check(application, USER_ID, COIN)

# ✅ ETF günlük görevi (sabah 9:00 Türkiye saatiyle)
job_time = time(hour=6, minute=0, tzinfo=pytz.timezone("Europe/Istanbul"))
application.job_queue.run_daily(
    etf_daily_job,
    time=job_time,
    name="etf_daily_job"
)

# ===============================
# ✅ Uyanık Kalma (Render Free)
# ===============================
keep_alive()

# ===============================
# ✅ Botu çalıştır
# ===============================
if __name__ == "__main__":
    application.run_polling()
