# send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    # your email credentials
    smtp_server = 'smtprelay.ldc.com'
    smtp_port = 25
    username = 'bei_occontdocs2@ldc.com'

    # create message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # setup the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)

        # send the email
        text = msg.as_string()
        server.sendmail(username, to_email, text)

        # close the connection
        server.quit()

        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email: {e}')
