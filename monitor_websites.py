#####################################
######## Website Down Alerts ########
###### Dan Duran - GetCyber.Me ######
#####################################

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# List your websites here
websites = [
    'https://website1.com',
    'https://website2.com',
    # ...Add more as you please
]

# Email configuration
email_sender = 'alerts@domain.com'
email_receiver = 'alerts@domain.com'  # Replace with the recipient's email address
email_subject = 'Website status alert'
smtp_server = 'smtp.domain.com'
smtp_username = 'alerts@domain.com'
smtp_password = 'PASSWORD'  # Replace with the actual email account's password


def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(smtp_username, smtp_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email: {e}')

if __name__ == '__main__':
    failed_websites = []

    for website in websites:
        if not check_website(website):
            failed_websites.append(website)
            print(f'Website down: {website}')

    if failed_websites:
        email_body = f"The following websites are down:\n\n" + "\n".join(failed_websites)
        send_email(email_subject, email_body)
    else:
        print('All websites are up.')

# 5 min CRON: */5 * * * * /usr/bin/python3 /path/to/your/file/monitor_websites.py
