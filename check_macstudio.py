import requests
import smtplib
import os
from email.mime.text import MIMEText

# Config
URL = 'https://www.apple.com/fr/shop/refurbished/mac/mac-studio'

def check_availability():
    r = requests.get(URL)
    return 'Aucun produit ne correspond à votre recherche' not in r.text

def send_email():
    smtp_user = os.environ['SMTP_USER']
    smtp_pass = os.environ['SMTP_PASS']
    to_email = os.environ['EMAIL_TO']

    msg = MIMEText(f'Le Mac Studio reconditionné est disponible ici: {URL}')
    msg['Subject'] = 'ALERTE Mac Studio Reconditionné'
    msg['From'] = smtp_user
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.free.fr', 587)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, [to_email], msg.as_string())
    server.quit()

def send_sms():
    user = os.environ['FREE_MOBILE_USER']
    passwd = os.environ['FREE_MOBILE_PASS']
    sms_url = f'https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={passwd}&msg=Mac+Studio+reconditionné+disponible'
    requests.get(sms_url)

def main():
    if check_availability():
        send_email()
        send_sms()
        print('Alerte envoyée.')
    else:
        print('Mac Studio non dispo.')

if __name__ == '__main__':
    main()

