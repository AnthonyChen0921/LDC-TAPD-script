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

    # extract first story_data
    fst_story_data = stories_data[0]
    # extract modified_date field
    fst_story_modified_date = fst_story_data['modified']
    # save only yyyy-mm-dd, pruning the time
    last_email_time = fst_story_modified_date.split(' ')[0]
    
    print(f"last_email_time: {last_email_time}")

    
    stories_content = ""
    subject_content = f"【TAPD日结】{last_email_time} 待处理Case:"

    for story_data in stories_data:
        # trim to preserve last 7 char of story_id
        story_id_short = story_data["id"][-7:]

        # create the link
        link = f'https://www.tapd.cn/fastapp/jump.php?target=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F{story_data["id"]}%3Fjump_count%3D1'

        stories_content += f"""
            <!--<h5>【ID{story_id_short}】{story_data["name"]} - FN处理中</h5>-->
            <p class="caption"><a href="{link}">{story_data["name"]}</a></p>
            <!--<hr>   this line will separate each story -->
        """
        # subject_content += f'【ID{story_id_short}】{story_data["name"]} - 待确认; '

    subject_content = subject_content.rstrip('; ')  # Remove trailing semicolon and space

    # prepare email content
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
                        p.text{{
                            color: #666;
                            font-size: 18px;
                        }}
                        p.caption {{
                            color: #999;
                            font-size: 16px;
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
                        <p class="text"> Hi, 早上好,以下是昨天的日结:</p>
                        <p class="caption"> (以下Case为FN处理中, 且24小时内有修改/跟进/需求/评论的Case, 请关注以下Case并及时处理,谢谢!)</p>
                        <br>
                        {stories_content}
                        <br>
                        <p class="text">感谢一直以来对运维, 以及对我们的技术支持, 谢谢!</p>
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
