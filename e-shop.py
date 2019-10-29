import logging
import logging.handlers
import os
import sys
import time
from io import StringIO
from subprocess import DEVNULL, call

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Eshop:
    """ E-shop automated navigator """

    def __init__(self):
        super(Eshop, self).__init__()
        self.msg = ''
        self.chrome_driver_path = os.path.join(os.getcwd(), 'Selenium', "chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.options.add_argument('log-level=3')
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(self.chrome_driver_path, options=self.options)
        self.shop_url = "https://arduino-shop.cz"
        self.verif_value = b'2 998,00 K\xc4\x8d'
        self.execution()
        self.teardown()

    def execution(self):
        self.log_update('info', "Launching automation scenario")
        self.log_update('info', "Opening web page: {}".format(self.shop_url))

        for i in range(2):
            try:
                self.driver.get(self.shop_url)
                self.log_update('info', 'Opened {} successfully'.format(self.shop_url))
                self.item_click_by_xpath('//*[@id="cssmenu_arduino_cz"]/ul/li[1]/a/span[2]')
                self.log_update('info', 'Navigated to menu by xpath')

                self.item_click_by_xpath('//*[@id="cssmenu_arduino_cz"]/ul/li[1]/ul/li[1]/a')
                self.log_update('info', 'Navigated to submenu by xpath')

                self.item_click_by_xpath('//*[@id="box-nad-produkty"]/div[2]/form/button[4]')
                self.log_update('info', 'Filtering in DESC order by price enabled')

                self.item_click_by_xpath('//*[@id="product-list-col-5401"]/div/div[3]/form/button')
                self.log_update('info', 'First item added')

                self.item_click_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[2]/div[1]/button')
                self.log_update('info', 'Navigated back successfully')

                self.item_click_by_xpath('//*[@id="product-list-col-5181"]/div/div[3]/form/button')
                self.log_update('info', 'Second item added, checking cart...')

                self.item_click_by_xpath('/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/a')

                element = self.driver.find_elements_by_xpath('//*[@id="celkova_cena"]')
                if element[0].text.encode("utf-8") == self.verif_value:
                    self.log_update('info', 'Test finished successfully')
                    break
            except Exception as ex:
                self.log_update('error', 'Exception during execution: {}'.format(ex))

    def item_click_by_xpath(self, xpath, timeout=10):
        item = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        item.click()

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

    def terminate_program(self, name):
        """ Terminate program by name """
        self.log_update('debug', 'Closing application {}'.format(name))
        call(['taskkill', '/IM', '{}*'.format(name), '/T', '/F'], stdout=DEVNULL, stderr=DEVNULL)
        self.log_update('debug', 'Application {} was closed'.format(name))

    def teardown(self):
        self.driver.close()
        self.terminate_program('chromedriver')


if __name__ == '__main__':
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

    sys.exit()
