import requests
import os.path
import smtplib

# --- SETTING ---
#LINK = "https://infostudenti.unitn.it/it/ammissione-corsi-laurea-studi-umanistici-marzo-21-22"
LINK = "https://infostudenti.unitn.it/it/ammissione-corsi-laurea-ingegneria-tecnico-scientifico-marzo-21-22"
COURSE = 'informatica'

SMTP_EMAIL = '<privacy>'
SMTP_PASSWORD = '<privacy>'
SMTP_HOST = 'smtp.<privacy>'
SMTP_PORT = 587

EMAIL_SUBJECT = 'Graduatoria esami'
EMAIL_MESSAGE = """Hey! Proabilmente hanno pubblicato la graduatoria dei test di ingresso di {}.
Per raggiungere velocemente la pagina clicca {}"""
EMAIL_TEMPLATE = """From: Unofficial notifier <{}>
To: {}
Subject: {}
Content-Type: text/plain; charset=utf-8

{}
"""
# ---------------

def check():
    res = requests.get(LINK).text.lower()
    return "allegati" in res or "graduatoria {}".format(COURSE) in res

def main():
    # kill switch
    print("[1] Check kill switch")
    if os.path.isfile('stop'):
        print("Already sent")
        return

    # check if they are public
    print("[2] Check with infostudenti")
    if not check():
        print("Not yet published")
        return

    # kill future attemptions
    print("[3] Set kill switch")
    with open('stop', 'w') as f:
        pass

    # read emails
    print("[4] Reading emails")
    lines = []
    emails = []
    with open('emails.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '').strip()
        if line != '':
            emails.append(line)
    
    # setup smtp
    print("[5] Setupping (?) smtp server")
    s = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    s.starttls()
    s.login(SMTP_EMAIL, SMTP_PASSWORD)

    for email in emails:
        msg = EMAIL_TEMPLATE.format(SMTP_EMAIL, email, EMAIL_SUBJECT, 
              EMAIL_MESSAGE.format(COURSE, LINK))
        s.sendmail(SMTP_EMAIL, [email], msg)
        print("[6] Email sent to {}".format(email))

    print("[7] Finished")

if __name__ == '__main__':
    main()
