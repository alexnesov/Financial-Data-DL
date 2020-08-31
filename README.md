# Finviz-Elite-financials-downloader-bot
I wanted to build my own database of historical indicators and financials, day after day. But logging every day and manually downloading the csv’s was tedious. So I decided to create this bot.

It opens a new chrome window, accepts the cookies to be able to navigate further. It then logs into my account (enters the password and the username).
Then, it clicks on every desired type of indicators and financials to download, downloads them, renames them. Finally, when they arrive to my local machine, it places them in the desired folder (they get also automatically renamed with today’s date).


<strong>Regarding AWS crontab. Cron command: </strong>

```
0 22 * * * cd ~/financials-downloader-bot && python3 run.py -e 'email' -p 'pass_word' > ~/financials-downloader-bot/crontab.log 2>&1
```
