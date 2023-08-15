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


def send_email_via_smtp(bcc_recipients, subject, body):
    # SMTP server details
    smtp_server = "smtprelay.ldc.com"
    smtp_port = 25
    username = "asi-navigator@ldc.com"

    # Create the MIMEText object for email body
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = username  # Since we're using BCC, we'll set the TO header to the sender
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

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

    send_email_via_smtp(test_emails, "test", "tset")


email()