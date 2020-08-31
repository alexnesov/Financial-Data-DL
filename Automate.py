from webbot import Browser 
import os
from datetime import datetime, timedelta 
from time import gmtime, strftime
import time
import subprocess,io
import shutil
import sys
import argparse


pairs = [
    ('Valuation','https://elite.finviz.com/screener.ashx?v=121'),
    ('Financial','https://elite.finviz.com/screener.ashx?v=161'),
    ('Ownership','https://elite.finviz.com/screener.ashx?v=131'),
    ('Performance','https://elite.finviz.com/screener.ashx?v=141'),
    ('Technical','https://elite.finviz.com/screener.ashx?v=171')
]


def directory_check():
    """
    Creates a data folder in root (__file__) if it doesn't exist 
    and downloads initial data to be able to display something at first program usage
    """
    if not os.path.exists(f"{os.path.dirname(os.path.realpath(__file__))}/US_STOCKS"):
        print("Creating the US_STOCKS directory in root. . .")
        os.mkdir(os.path.dirname(os.path.realpath(__file__))+ "/US_STOCKS")
        time.sleep(1)
    else:
        pass


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
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            # os.startfile(newdir) (WINDOWS)
            os.system('xdg-open "%s"' % newdir) # (LINUX)
            print('Old directory successfully replaced!')
        else:
            CONTINUE = "no"
            print('Process stoped.')
            sys.exit()
    else:
        os.mkdir(f'{newdir}')
        time.sleep(1)
        # os.startfile(newdir) (WINDOWS)
        os.system('xdg-open "%s"' % newdir) # (LINUX)

        print('Directory Created!')       


def initilization(**credentials):
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
    web.type(credentials['EMAIL'], number=1) # "number 1" refers to the first field, i.e the email"
    web.type(credentials['PASS'], into='Your password')
    web.click('Log in')
    web.go_to('https://elite.finviz.com/screener.ashx?v=111')
    web.click('export')
    time.sleep(2) 
    os.rename(f'{PATH_DL}/finviz.csv',f'{newdir}/Overview.csv')


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
        os.rename(f'{PATH_DL}/finviz.csv',f'{newdir}/{name}.csv')
        print(f'Success for: {name} !')



def main():
    global PATH_TARGET
    global web
    global PATH_DL
    directory_check()
    PATH_DL = '/home/nesovic/Downloads'
    PATH_TARGET = f'{os.path.dirname(os.path.realpath(__file__))}' + '/US_STOCKS'
    CONTINUE = "yes"
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", dest="EMAIL",
                        type=str, required=True)
    parser.add_argument("-p", "--pass", dest="PASS",
                        type=str, required=True)
    args = parser.parse_args()
    credentials = args.__dict__
    set_daily_directory()
    if CONTINUE == "yes":
        web = Browser()
        initilization(**credentials)
        loop()
    else:
        sys.exit()


if __name__ == "__main__":
    main()
