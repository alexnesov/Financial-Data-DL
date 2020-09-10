# -*- coding: utf-8 -*-

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

url = 'https://www.finviz.com/'

pairs = [
    ('Valuation', 'https://elite.finviz.com/screener.ashx?v=121'),
    ('Financial', 'https://elite.finviz.com/screener.ashx?v=161'),
    ('Ownership', 'https://elite.finviz.com/screener.ashx?v=131'),
    ('Performance', 'https://elite.finviz.com/screener.ashx?v=141'),
    ('Technical', 'https://elite.finviz.com/screener.ashx?v=171')
]


def get_data(url, **credentials):
    # options = ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--gpu-disabled")
    # browser = webdriver.Chrome(chrome_options=options)

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
    options.headless = True
    browser = webdriver.Firefox(options=options, capabilities=firefox_capabilities)

    browser.get(url)
    browser.find_element_by_link_text("Login").click()
    browser.find_element_by_name('email').send_keys(credentials['email'])
    browser.find_element_by_name('password').send_keys(credentials['password'])
    browser.find_element_by_css_selector("input.button").click()

    for name, url in pairs:
        browser.get(url)
        browser.find_element_by_link_text("export").click()
        time.sleep(2)
        # Here the CSV is downloaded from the website, but the next line doesn't make sense in AWS context, because it's
        # not downloaded into my computer, but rather, in the cloud.
        os.rename(os.path.join(download_dir, 'finviz.csv'), os.path.join(download_dir, '{name}_{date}.csv'.format(name=name, date=today)))
        print('Success for: {name}_{today} !'.format(name=name, today=today))

    browser.quit()


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
