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


# Configuring logging
logging.basicConfig(filename="emailbot.log", 
                    format='%(asctime)s [%(levelname)s]: %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)  # Change to logging.DEBUG for more detailed logs

def save_last_email_time():
    with open("last_email_time.txt", 'w') as file:
        file.write(str(last_email_time))

def read_last_email_time():
    try:
        with open("last_email_time.txt", 'r') as file:
            timestamp = file.read()
            return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except (FileNotFoundError, ValueError):
        return None

# Load configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Load cookies from cookies.json
with open(config['file_names']['cookie_file'], 'r') as f:
    cookie_list = json.load(f)

workspace_id = config["workspace_id"]

def load_email_map(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def autoClose():
    # load the previously fetched data
    try:
        with open(config['file_names']['story_file'], 'r') as file:
            stories = json.load(file)
    except FileNotFoundError:
        stories = {}

    threshold_date = datetime.datetime.now() - datetime.timedelta(days=config["threshold_days"])

    for story_id, story_data in stories.items():
        modified_date = datetime.datetime.strptime(story_data['modified'], "%Y-%m-%d %H:%M:%S")
        
        if modified_date < threshold_date:
            logging.info(f"Closing story {story_id}")  # Logging the auto close action
            close_story(workspace_id, story_id, cookie_list)

def autoFillOwner():
    # load the previously fetched data
    try:
        with open(config['file_names']['story_file'], 'r') as file:
            stories = json.load(file)
    except FileNotFoundError:
        stories = {}

    # Check for empty owners and print them
    for story_id, story_data in stories.items():
        owner = story_data.get('owner', '').strip()  # get the owner and strip any whitespace
        creator = story_data.get('creator', 'Unknown creator')  # get the creator or default to 'Unknown creator' if not present
        if not owner:  # check if owner is empty
            print(f"Story ID {story_id} has an empty owner. Created by {creator}.")
            logging.info(f"Assigning owner of story {story_id} with creator {creator}")  # Logging the assignment
            change_owner(workspace_id, story_id, cookie_list, creator)


def classify():
    # fetch unclassified data
    fetch_story_unclassified(workspace_id, cookie_list)

    # Load data from unclassified_story.json
    with open(config['file_names']['unclassified_story_file'], 'r') as f:
        stories_data = json.load(f)

    # Check each story
    for story_id, story_data in stories_data.items():
        story_name = story_data.get('name', '')
        if story_name.startswith("Case-"):
            print(f"not classified {story_id} and {story_name}")
            logging.info(f"Classifying story {story_id} with title: '{story_name}' to Production Case")  # Logging the classification
            classify_story(workspace_id, story_id, cookie_list)

def email():
    # load the previously fetched data
    try:
        with open(config['file_names']['story_file'], 'r') as file:
            old_data = json.load(file)
    except FileNotFoundError:
        old_data = {}

    # fetch the current data
    current_data_dict = fetch_story(workspace_id, cookie_list, 1)

    # save the current data to a file for future comparison
    with open(config['file_names']['story_file'], 'w') as file:
        json.dump(current_data_dict, file)

    # check for changes in status from "status_3" to "status_7"
    for story_id, story_data in current_data_dict.items():
        old_story_data = old_data.get(story_id)
        if old_story_data is None:
            continue

        if old_story_data['status'] == 'status_3' and story_data['status'] == 'status_7':
            # send email
            # Load email mapping
            email_map = load_email_map(config['file_names']['email_map_file'])

            # Parse the owners and remove any empty strings after splitting
            owners = [owner.strip() for owner in story_data['owner'].split(';') if owner.strip()]
            print(f"Found owners: {owners}")

            recipient_emails = []
            for owner in owners:
                emails = email_map.get(owner)
                if emails:
                    recipient_emails.append(emails)
                    print(f"Found recipients for owner: {owner}")
                else:
                    logging.warning(f"No recipients found for for owner: {owner}. Consider add to contact.json manually")
                    print(f"⚠️ No recipients found for owner: {owner}")

            print(f"Found recipient emails: {recipient_emails}")
            if recipient_emails:
                cc_emails = ['erdong.chen-ext@ldc.com', 'alan.pei@ldc.com']
                logging.info(f"Sending email to {recipient_emails} with CC {cc_emails} for story {story_data['id']}")  # Logging the email action
                send_email(recipient_emails, cc_emails, story_data)
            else:
                logging.warning("No recipients found for the given owners.")


def emailRemainder_FN():
    TO_EMAILS = ["erdong.chen-ext@ldc.com", "recipient2@example.com"]
    CC_EMAILS = ["erdong.chen-ext@ldc.com", "cc2@example.com"]

    # Load the stories data
    try:
        with open(config['file_names']['story_file'], 'r') as file:
            stories = json.load(file)
    except FileNotFoundError:
        stories = {}

    # Calculate the threshold date, which is 24 hours ago
    threshold_date = datetime.datetime.now() - datetime.timedelta(hours=24)

    # Check if the current time is 9:00 am
    current_time = datetime.datetime.now().time()
    print(current_time)

    if current_time.hour == 14 and current_time.minute == 54:
        stories_to_send = []
        for story_id, story_data in stories.items():
            # Convert the modified date from string to datetime
            modified_date = datetime.datetime.strptime(story_data['modified'], "%Y-%m-%d %H:%M:%S")

            if modified_date > threshold_date and story_data["status"] == 'status_3':
                stories_to_send.append(story_data)

        # Now, send these stories through email
        if stories_to_send:
            print("email fn sent")
            send_email_for_stories(TO_EMAILS, CC_EMAILS, stories_to_send)



logging.info(f"Starting script at {datetime.datetime.now()}")  # Logging the start of the script

# run the main function every sleep_time seconds
while True:
    try:
        if config["control_flags"]["email"]:
            email()
        if config["control_flags"]["classify"]:
            classify()
        if config["control_flags"]["autoClose"]:
            autoClose()
        if config["control_flags"]["autoFillOwner"]:
            autoFillOwner()
        if config["control_flags"]["emailRemainder_FN"]:
            emailRemainder_FN()
        
    except Exception as e:
        logging.error(f"Encountered an error: {str(e)} but continue running.")
    # Optionally re-raise the exception if you want to see the traceback or debug it
    # raise e
    
    time.sleep(config['api']['sleep_time'])