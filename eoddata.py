# -*- coding: utf-8 -*-
#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import argparse
from datetime import datetime
today = str(datetime.today().strftime('%Y-%m-%d'))


url = 'http://www.eoddata.com/'


def get_data(url, **credentials):
    
    dir_name, file_name = os.path.split(os.path.abspath(__file__))
    download_dir = os.path.join(dir_name, 'downloads')
    print("Downloads directory:", download_dir)

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_dir)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    options = FirefoxOptions()
    options.profile = fp
    options.headless = False
    browser = webdriver.Firefox(options=options, capabilities=firefox_capabilities)

    browser.get(url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", dest="email",
                        type=str, required=True)
    parser.add_argument("-p", "--password", dest="password",
                        type=str, required=True)
    args = parser.parse_args()
    credentials = args.__dict__
    get_data(url, **credentials)


if __name__ == '__main__':
    main()

