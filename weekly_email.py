import time
import json
import logging
import datetime
from fetch_story import fetch_story
from send_email import send_email
from classify_story import classify_story
from fetch_story_unclassified import fetch_story_unclassified
from change_owner import change_owner
from close_story import close_story
from send_email_FN import send_email_for_stories
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Configuring logging
logging.basicConfig(filename="emailbot.log", 
                    format='%(asctime)s [%(levelname)s]: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)  # Change to logging.DEBUG for more detailed logs


# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Load cookies from cookies.json
with open(config['file_names']['cookie_file'], 'r') as f:
    cookie_list = json.load(f)

workspace_id = config["workspace_id"]


def send_email_via_smtp(bcc_recipients):
    # SMTP server details
    smtp_server = "smtprelay.ldc.com"
    smtp_port = 25
    username = "asi-navigator@ldc.com"

    # Constructing the HTML message
    html_message = """
    <html>
    <head></head>
    <body>
        <p>Hi all,</p>
        <br>
        <p>请每天关注TAPD平台中工作台部分的“我的待办”，如果生产case符合以下上三个状态的，请及时更新状态并“流转”。</p>
        <ul>
            <li>关闭（已处理）</li>
            <li>关闭（转长期追踪）</li>
            <li>关闭（转需求）</li>
        </ul>
        <p>如果对处理结果不满意的，请将“处理人”还原为上一位富农产品/开发/测试的名字，并将状态更新为“FN处理中”。</p>
        <p>对以上操作，有任何疑问的，请随时联系我/Chiling, 谢谢。</p>
        <br>
        <p>Best Regards,</p>
        <br>
        <img src="data:image/png;base64,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.png" alt="Signature">
    </body>
    </html>
    """

    # Create the MIMEText object for email body
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = username  # Since we're using BCC, we'll set the TO header to the sender
    msg['Subject'] = "【航海家系统】生产Case及时关闭"  # Set your desired subject here
    msg.attach(MIMEText(html_message, 'html'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:
            server.sendmail(username, [username] + bcc_recipients, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")


def email():
    # Load the current data
    current_data_dict = fetch_story(workspace_id, cookie_list, 1)

    # List to collect all owner 'custom_field_two' values
    custom_field_two_list = []

    # Loop through the current data to check status and collect 'custom_field_two' values
    for story_id, story_data in current_data_dict.items():
        if story_data['status'] == 'status_7':
            custom_field_two_list.extend(story_data['custom_field_two'].split(';'))

    # Strip unwanted characters and ignore empty fields
    custom_field_two_list = [name.strip(';').strip() for name in custom_field_two_list if name.strip()]

    # Load email mapping from contact.json
    try:
        with open(config['file_names']['email_map_file'], 'r') as file:
            email_map = json.load(file)
    except FileNotFoundError:
        logging.error("Error: contact.json not found!")
        return

    recipient_emails_set = set()  # using a set to avoid duplicates
    test_emmails_set=set()
    for custom_field in custom_field_two_list:
        # Get the email from the email_map
        email_address = email_map.get(custom_field)
        if email_address:
            recipient_emails_set.add(email_address)
        # removed the warning as per your instruction

    # Convert the set back to a list
    recipient_emails = list(recipient_emails_set)
    test_emmails_set.add("Erdong.Chen-EXT@ldc.com")
    test_emails=list(test_emmails_set)
    print(f"Found recipient emails: {test_emmails_set}")

    send_email_via_smtp(test_emails)


email()