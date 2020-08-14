
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime, timedelta 
from time import gmtime, strftime
import time



PATH_DL = 'C:\\Users\\alexa\\Downloads'
PATH_TARGET = f'C:\\Users\\alexa\\OneDrive\\Desktop\\Finviz downloads\\US_STOCKS'

url = 'https://www.finviz.com/'

pairs = [
    ('Valuation','https://elite.finviz.com/screener.ashx?v=121'),
    ('Financial','https://elite.finviz.com/screener.ashx?v=161'),
    ('Ownership','https://elite.finviz.com/screener.ashx?v=131'),
    ('Performance','https://elite.finviz.com/screener.ashx?v=141'),
    ('Technical','https://elite.finviz.com/screener.ashx?v=171')
]


def set_daily_directory():
    """
    1. This function takes today's date and formats it to fit the old folders names
    2. A new directory is created with this newly created name
    """
    global newdir
    today = str(datetime.today().strftime('%Y-%m-%d'))
    splitted = today.split('-')
    year, month, day = splitted[0],splitted[1],splitted[2]
    new = "US_STOCKS"+'_'+str(day)+'_'+str(month)+'_'+str(year)
    newdir = os.path.join(PATH_TARGET, f'{new}') 
    if os.path.exists(newdir): #(if True)
        response = input('A directory with today\'s date already exists, do you want to replace it? (y or n?)')
        if response == "y" or "yes" or "Y":
            shutil.rmtree(newdir)
        os.makedirs(newdir)
        os.startfile(newdir)
        print('Old directory successfully replaced!')
    else:
        os.mkdir(f'{newdir}')
        os.startfile(newdir)
        print('Directory Created!')    


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
        os.rename(f'{PATH_DL}\\finviz.csv',f'{newdir}\\{name}.csv')
        print(f'Success for: {name} !')


if __name__ == '__main__':
    EMAIL = os.environ.get('USER_FINVIZ')
    PASSWORD = os.environ.get('PASS_FINVIZ')
    set_daily_directory()
    get_data(url)
