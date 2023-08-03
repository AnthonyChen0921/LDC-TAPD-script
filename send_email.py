# send_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data['id']}%3Fjump_count%3D1


def send_email(to_emails, cc_emails, story_data):
    # your email credentials
    smtp_server = "smtprelay.ldc.com"
    smtp_port = 25
    username = "bei_occontdocs2@ldc.com"

    # trim to perserve last 7 char of story_id
    story_id_short = story_data["id"][-7:]

    # create the link
    link = f'https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data["id"]}%3Fjump_count%3D1'
    hyperlink_format = f'<a href="{link}">{story_data["name"]}</a>'

    # prepare email content
    subject = f'【ID{story_id_short}】{story_data["name"]} - 待确认'
    body = f""" 
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                            }}
                            .content {{
                                margin: auto;
                                width: 90%;
                                padding: 10px;
                                border: 1px solid #ddd;
                                border-radius: 5px;
                                background-color: #f9f9f9;
                            }}
                            h1 {{
                                color: #333;
                            }}
                            p {{
                                color: #666;
                            }}
                            a.button {{
                                display: inline-block;
                                color: white;
                                background-color: #3498db;
                                padding: 10px 15px;
                                text-align: center;
                                border-radius: 5px;
                                text-decoration: none;
                                margin: 10px 0;
                            }}
                            a.button:hover {{
                                background-color: #2980b9;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="content">
                            <h1>【ID{story_id_short}】{story_data["name"]} - 待确认</h1>
                            <p>【ID{story_id_short}】 ({story_data["name"]}, created by {story_data["creator"]}) 已从 "FN处理中" 变更为 "LDC确认中". 请尽快前往确认：</p>
                            <p><a href="{link}">{story_data["name"]}</a></p>
                            <a class="button" href="{link}">Click here</a>
                            <p>如果对处理结果不满意的, 请将“处理人”还原为上一位富农产品/开发/测试的名字, 并将状态更新为“FN处理中”。</p>
                        </div>
                    </body>
                </html>
            """

    


    # create message
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
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

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
