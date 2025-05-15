import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIG --- #
URL = "https://www.apple.com/fr/shop/refurbished/mac-studio"  # URL à checker
KEYWORD = "Mac Studio"  # Mot clé à détecter

# Mail
SMTP_SERVER = "smtp.free.fr"
SMTP_PORT = 587
SMTP_USER = "guilaind@free.fr"
SMTP_PASS = "La3emePorte"

MAIL_FROM = SMTP_USER
MAIL_TO = "guilaind@free.fr"

# Free Mobile API SMS
FREE_MOBILE_USER = "+33613592685"    # numéro client Free Mobile (ou identifiant)
FREE_MOBILE_API_KEY = "rHqSroj5TjLeNP"

# --- FONCTIONS --- #

def check_page():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Erreur de connexion à la page")
        return False
    return KEYWORD in response.text

def send_mail(subject, body):
    msg = MIMEText(body)
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg["Subject"] = subject

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
    print("Mail envoyé")

def send_sms(message):
    url = f"https://smsapi.free-mobile.fr/sendmsg?user={FREE_MOBILE_USER}&pass={FREE_MOBILE_API_KEY}&msg={message}"
    r = requests.get(url)
    if r.status_code == 200:
        print("SMS envoyé")
    else:
        print(f"Erreur envoi SMS: {r.status_code} {r.text}")

# --- MAIN --- #

if __name__ == "__main__":
    if check_page():
        subject = "Mac Studio disponible"
        body = f"Le Mac Studio est disponible ici : {URL}"
        send_mail(subject, body)
        send_sms(body)
    else:
        print("Mot clé non trouvé, rien envoyé.")
