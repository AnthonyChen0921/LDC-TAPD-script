# send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
# Configuring logging
logging.basicConfig(filename="emailbot.log", 
                    format='%(asctime)s [%(levelname)s]: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)  # Change to logging.DEBUG for more detailed logs

# https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data['id']}%3Fjump_count%3D1


def send_email_for_stories(to_emails, cc_emails, stories_data):
    # your email credentials
    smtp_server = "smtprelay.ldc.com"
    smtp_port = 25
    username = "asi-navigator@ldc.com"
    
    stories_content = ""
    subject_content = ""

    for story_data in stories_data:
        # trim to preserve last 7 char of story_id
        story_id_short = story_data["id"][-7:]

        # create the link
        link = f'https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data["id"]}%3Fjump_count%3D1'

        stories_content += f"""
            <h1>【ID{story_id_short}】{story_data["name"]} - 待确认</h1>
            <p class="text">【ID{story_id_short}】 ({story_data["name"]}, created by {story_data["creator"]}) 已从 "FN处理中" 变更为 "LDC确认中". 请尽快前往确认：</p>
            <hr>  <!-- this line will separate each story -->
        """
        subject_content += f'【ID{story_id_short}】{story_data["name"]} - 待确认; '

    subject_content = subject_content.rstrip('; ')  # Remove trailing semicolon and space

    # prepare email content
    body = f""" 
            <html>
                <head>
                    <!-- ... (styles unchanged from previous code) ... -->
                </head>
                <body>
                    <div class="content">
                        {stories_content}
                        <p class="text">如果对处理结果不满意的, 请将“处理人”还原为上一位富农产品/开发/测试的名字, 并将状态更新为“FN处理中”。</p>
                        <p class="caption">如有疑问请联系Alan</p>
                    </div>
                </body>
            </html>
        """

    # create message
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject_content  # Adjusted subject to include all story names
    msg.attach(MIMEText(body, "html"))

    try:
        # setup the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)

        # list of all recipients
        all_recipients = to_emails + cc_emails

        # send the email
        text = msg.as_string()
        server.sendmail(username, all_recipients, text)

        # close the connection
        server.quit()

        logging.info("Email remainder sent to FN successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
