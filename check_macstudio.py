import os
import requests
import smtplib
from email.mime.text import MIMEText

# Config
EMAIL_TO = os.environ["EMAIL_TO"]
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]
FREE_MOBILE_USER = os.environ["FREE_MOBILE_USER"]
FREE_MOBILE_PASS = os.environ["FREE_MOBILE_PASS"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())
        print("📧 Email sent")

def send_sms(message):
    url = f"https://smsapi.free-mobile.fr/sendmsg"
    payload = {
        "user": FREE_MOBILE_USER,
        "pass": FREE_MOBILE_PASS,
        "msg": message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("📱 SMS sent")
    else:
        print(f"❌ Failed to send SMS: {response.status_code} - {response.text}")

def main():
    url = "https://www.apple.com/fr/shop/refurbished/mac.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch data: {response.status_code}")
        return

    refurb_data = response.json()
    if not refurb_data:
        print("No refurbished products available.")
        return

    found = False
    for product in refurb_data:
        name = product.get("name", "").lower()
        print(f"🔍 Checking: {name}")
        if "mac studio" in name:
            print("✅ Mac Studio refurb found!")
            url = "https://www.apple.com/fr/shop/refurbished/mac/mac-studio"
            send_email("Mac Studio Refurb Found!", f"Dispo ici : {url}")
            send_sms("Mac Studio refurb dispo !")
            found = True
            break

    if not found:
        print("No Mac Studio found.")

if __name__ == "__main__":
    main()
