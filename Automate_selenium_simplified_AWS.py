
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime, timedelta 
from time import gmtime, strftime
import time

url = 'https://www.finviz.com/'

pairs = [
    ('Valuation','https://elite.finviz.com/screener.ashx?v=121'),
    ('Financial','https://elite.finviz.com/screener.ashx?v=161'),
    ('Ownership','https://elite.finviz.com/screener.ashx?v=131'),
    ('Performance','https://elite.finviz.com/screener.ashx?v=141'),
    ('Technical','https://elite.finviz.com/screener.ashx?v=171')
]


def get_data(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    browser.find_element_by_link_text("Login").click()
    browser.find_element_by_name('email').send_keys(EMAIL)
    browser.find_element_by_name('password').send_keys(PASSWORD)
    browser.find_element_by_css_selector("input.button").click()
    
    for name, url in pairs:
        browser.get(f'{url}')
        browser.find_element_by_link_text("export").click()
        time.sleep(2) 
        # Here the CSV is downloaded from the website, but the next line doesn't make sense in AWS context, because it's 
        # not downloaded into my computer, but rather, in the cloud.
        os.rename(f'{PATH_DL}\\finviz.csv',f'{newdir}\\{name}.csv')
        print(f'Success for: {name} !')


if __name__ == '__main__':
    EMAIL = os.environ.get('USER_FINVIZ')
    PASSWORD = os.environ.get('PASS_FINVIZ')

