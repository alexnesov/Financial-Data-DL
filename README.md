# Finviz-Elite-financials-downloader-bot
I wanted to build my own database of historical indicators and financials, day after day. But logging every day and manually downloading the csv’s was tedious. So I decided to create this bot.

It opens a new chrome window, accepts the cookies to be able to navigate further. It then logs into my account (enters the password and the username).
Then, it clicks on every desired type of indicators and financials to download, downloads them, renames them. Finally, when they arrive to my local machine, it places them in the desired folder (they get also automatically renamed with today’s date).

I ended up by pushing the code into the cloud (AWS EC2 instance) and scheduled a cron job in the linux environnement.

<strong>Regarding AWS EC2 crontab. Cron command: </strong>

```
0 22 * * * cd ~/financials-downloader-bot && python3 run.py -e 'email' -p 'pass_word' > ~/financials-downloader-bot/crontab.log 2>&1
```


<h4>Steps to reproduce to be able to</h4>

First, allow unsecure connections on your gmail account.
Here: https://myaccount.google.com/lesssecureapps

<strong>Setup:</strong>

```
sudo apt-get install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules
```

<strong> Open postfix config </strong>

```
nano /etc/postfix/main.cf
```

Add this:
```
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
smtp_use_tls = yes
```

<strong>Adding gmail pass and username:</strong>

```
nano /etc/postfix/sasl_passwd
```
--> ```[smtp.gmail.com]:587    USERNAME@gmail.com:PASSWORD```


<strong>Giving permissions:</strong>
```
sudo chmod 400 /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
```

<strong>Run this:</strong>

```
cat /etc/ssl/certs/ca-certificates.crt | sudo tee -a /etc/postfix/cacert.pem

```

<strong> Reload: </strong>

```
sudo /etc/init.d/postfix reload
```

<strong>Check</strong>
```
echo "Test mail from ubuntu" | mail -s "Testing Setup" you@example.com 
```

Help: http://mhawthorne.net/posts/2011-postfix-configuring-gmail-as-relay/
