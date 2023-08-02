# send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data['id']}%3Fjump_count%3D1

def send_email(to_email, story_data):
    # your email credentials
    smtp_server = 'smtprelay.ldc.com'
    smtp_port = 25
    username = 'bei_occontdocs2@ldc.com'

    # trim last 7 char of story_id
    story_id_short = story_data['id'][:-7]

    # prepare email content
    subject = f'【ID{story_id_short}】{story_data["name"]}待确认'
    body = f"""
                【ID{story_id_short}】 ({story_data["name"]}, created by {story_data["creator"]}) 已从 "FN处理中" 变更为 "LDC确认中". 请尽快前往确认：
                https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data['id']}%3Fjump_count%3D1
                如果对处理结果不满意的，请将“处理人”还原为上一位富农产品/开发/测试的名字, 并将状态更新为“FN处理中”。
            """

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
