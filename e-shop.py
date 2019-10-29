import logging
import logging.handlers
import os
import sys
import time
from io import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Eshop:
    """ Jira Ticket Automated Calculator Class """

    def __init__(self):
        super(Eshop, self).__init__()
        self.chrome_driver_path = os.path.join(os.getcwd(), 'Selenium', "chromedriver.exe")
        self.msg = ''
        self.shop_url = "https://www.alza.cz/"

    def execution(self):
        self.log_update('info', "Launching scenario")
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('log-level=3')
        driver = webdriver.Chrome(
            self.chrome_driver_path, options=options)
        self.log_update('info', "Opening web page: {}".format(self.shop_url))

    def log_update(self, level, msg):
        if level == 'critical' and logger.level <= 50:
            logging.critical(msg)
            self.update_log(level, msg)
        elif level == 'error' and logger.level <= 40:
            logging.error(msg)
            self.update_log(level, msg)
        elif level == 'warning' and logger.level <= 30:
            logging.warning(msg)
            self.update_log(level, msg)
        elif level == 'info' and logger.level <= 20:
            logging.info(msg)
            self.update_log(level, msg)
        elif level == 'debug' and logger.level == 10:
            logging.debug(msg)
            self.update_log(level, msg)

    def update_log(self, level, msg):
        self.msg += '{} | {} | {}\n'.format(time.strftime("%Y-%m-%d %H:%M %p"), level, msg)


if __name__ == '__main__':
    print("Launched successfully")
    os.makedirs('Logs', exist_ok=True)
    logger = logging.getLogger()
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    fh = logging.handlers.RotatingFileHandler('Logs/app.log', maxBytes=20480, backupCount=30)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.fatal('-----------------------------------------------------------------------------')

    ESHOPAUTOMATION = Eshop()

    # sys.exit()
