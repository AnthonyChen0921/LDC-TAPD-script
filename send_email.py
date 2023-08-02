# send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F1155989309001001871%3Fjump_count%3D1

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
