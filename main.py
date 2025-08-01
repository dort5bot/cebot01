###main.py 4+etf

import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

# Dosya sistemini hazırla
from utils.init_files import init_data_files
from keep_alive import keep_alive

init_data_files()
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot uygulaması
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Komut handler'ları
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
application.add_handler(etf_handler())
application.add_handler(fr_handler())
application.add_handler(al_handler())
application.add_handler(sat_handler())
application.add_handler(stop_handler())
application.add_handler(aktif_handler())
application.add_handler(raporum_handler())
application.add_handler(apikey_handler())

# JobQueue görevleri
from jobs.check_orders import schedule_order_check
from jobs.fr_scheduler import schedule_fr_check

schedule_order_check(application.job_queue)

# İsteğe bağlı kullanıcı ve coin örneği (kendi ID ve coin ile değiştir)
USER_ID = 123456789  # Değiştir
COIN = "BTC"         # Değiştir

schedule_fr_check(application, USER_ID, COIN)

# Render keep_alive
keep_alive()

# Botu başlat
if __name__ == "__main__":
    application.run_polling()
