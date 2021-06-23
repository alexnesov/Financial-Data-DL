from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
import os
import time
from datetime import datetime
today = str(datetime.today().strftime('%Y-%m-%d'))



url = 'https://stocktwits.com/'


dir_path = os.path.dirname(os.path.realpath(__file__))


fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
#fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
options = FirefoxOptions()
options.profile = fp
options.headless = False
browser = webdriver.Firefox(options=options, capabilities=firefox_capabilities)


str_email = '***REMOVED***'
str_pass = '***REMOVED***'


browser.get(url)
browser.find_elements_by_class_name("lib_2cF8aMP")[0].click()
browser.find_element_by_name('login').send_keys(str_email)
browser.find_element_by_name('password').send_keys(str_pass)
time.sleep(2)
browser.find_element_by_name('password').send_keys(Keys.ENTER)



tradable_cyrpto_coinbase = ['ETH.X',
'EOS.X',
'BTC.X',
'USDT.X',
'ADA.X',
'DOGE.X',
'DOT.X',
'UNI.X',
'BCH.X',
'LTC.X',
'SOL.X',
'LINK.X']

for crypto_symbol in tradable_cyrpto_coinbase:
    tick_url = f'https://stocktwits.com/symbol/{crypto_symbol}'
    time.sleep(1)
    browser.get(tick_url)
    # Getting number of watchers
    watchers = browser.find_elements_by_class_name("st_HebiDD2")[0].text
    price = browser.find_elements_by_class_name("st_3zYaKAL")[0].text

    print(f"Number of watchers for: {crypto_symbol}: ", watchers)
    print("Price @ 3h Central Europe: ", price)
    time.sleep(2)

browser.quit()