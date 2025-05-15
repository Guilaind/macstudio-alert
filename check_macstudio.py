import requests
import smtplib
import os
from email.mime.text import MIMEText

# URL du rayon Mac Studio reconditionné sur apple.fr
APPLE_REFURB_URL = 'https://www.apple.com/fr/shop/refurbished/mac/mac-studio'

# Texte ou mot-clé à repérer (ajuste si Apple change leur page)
KEYWORDS = ['Mac Studio', 'Reconditionné']

def page_contains_mac_studio():
    response = requests.get(APPLE_REFURB_URL, timeout=10)
    response.raise_for_status()
    page_content = response.text
    return any(keyword.lower() in page_content.lower() for keyword in KEYWORDS)

def send_email(subject, body):
    smtp_user = os.environ['SMTP_USER']
    smtp_pass = os.environ['SMTP_PASS']
    recipient = os.environ['EMAIL_TO']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient

    with smtplib.SMTP('smtp.free.fr', 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [recipient], msg.as_string())

def send_sms(body):
    user = os.environ['FREE_MOBILE_USER']
    passwd = os.environ['FREE_MOBILE_PASS']
    payload = {
        'user': user,
        'pass': passwd,
        'msg': body
    }
    requests.post('https://smsapi.free-mobile.fr/sendmsg', data=payload)

if __name__ == '__main__':
    try:
        if page_contains_mac_studio():
            message = f"studio"
            send_email("Mac Studio Reconditionné Disponible", message)
            send_sms(message)
        else:
            print("Rien trouvé.")
    except Exception as e:
        print(f"Erreur : {e}")
