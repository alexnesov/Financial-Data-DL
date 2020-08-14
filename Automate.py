from webbot import Browser 
import os
from datetime import datetime, timedelta 
from time import gmtime, strftime
import time
import subprocess,io
import shutil
import sys

PATH_DL = 'C:\\Users\\alexa\\Downloads'
PATH_TARGET = f'C:\\Users\\alexa\\OneDrive\\Desktop\\Finviz downloads\\US_STOCKS'
CONTINUE = "yes"

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
    global CONTINUE
    today = str(datetime.today().strftime('%Y-%m-%d'))
    splitted = today.split('-')
    year, month, day = splitted[0],splitted[1],splitted[2]
    new = "US_STOCKS"+'_'+str(day)+'_'+str(month)+'_'+str(year)
    newdir = os.path.join(PATH_TARGET, f'{new}') 
    if os.path.exists(newdir): #(if True)
        response = input('A directory with today\'s date already exists, do you want to replace it? (y or n?)')
        possibilities = ["y","yes","Yes","YES"]
        if response in possibilities:
            CONTINUE = "yes"
            shutil.rmtree(newdir)
            os.makedirs(newdir)
            os.startfile(newdir)
            print('Old directory successfully replaced!')
        else:
            CONTINUE = "no"
            print('Process stoped.')
            sys.exit()
    else:
        os.mkdir(f'{newdir}')
        os.startfile(newdir)
        print('Directory Created!')       

def initilization():
    """
    This function is usefull before the loop to log into the website
    (Finviz elite needs an account) and also to remove the cookies popup
    """
    print("Sending https request...")
    web.go_to('https://elite.finviz.com/screener.ashx?v=111')
    time.sleep(2) 
    print("Accepting cookies..")
    web.click('Accept All') 
    web.click('Login')
    web.type(f'{EMAIL}' , number=1) # "number 1" refers to the first field, i.e the email"
    web.type(f'{PASSWORD}' , into='Your password')
    web.click('Log in')
    web.go_to('https://elite.finviz.com/screener.ashx?v=111')
    web.click('export')
    time.sleep(2) 
    os.rename(f'{PATH_DL}\\finviz.csv',f'{newdir}\\Overview.csv')

def loop():
    """
    We do the same thing as before minus the log and the popup removal,
    but for all the remaining downloads
    """
    for name, url in pairs:
        web.go_to(f'{url}') 
        web.click('export')
        # We set a 3 seconds sleep to let the system download the file, 
        #otherwise it will immeditaly go to rename, eventhough the dl not finished and hence yield an error
        time.sleep(3) 
        os.rename(f'{PATH_DL}\\finviz.csv',f'{newdir}\\{name}.csv')
        print(f'Success for: {name} !')


if __name__ == "__main__":
    EMAIL = os.environ.get('USER_FINVIZ')
    PASSWORD = os.environ.get('PASS_FINVIZ')
    set_daily_directory()
    if CONTINUE == "yes":
        web = Browser()
        initilization()
        loop()
    else:
        sys.exit()

