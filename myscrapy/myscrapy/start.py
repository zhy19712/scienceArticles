import sys
import os

from apscheduler.schedulers.background import BackgroundScheduler
from scrapy import cmdline


def run_scrapy():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_process, 'interval', minutes=1200)
    try:
        # scheduler.remove_all_jobs()
        scheduler.start()
    except (KeyboardInterrupt):
        pass
    start_process()
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    cmdline.execute('scrapy crawl ctg_spider'.split())