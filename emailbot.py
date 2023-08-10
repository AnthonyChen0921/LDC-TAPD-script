import time
import json
import datetime
from fetch_story import fetch_story
from send_email import send_email
from classify_story import classify_story
from fetch_story_unclassified import fetch_story_unclassified

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
            print(story_id)

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
            print(f"not classified {story_id} and {story_data}")
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
                    print(f"⚠️ No recipients found for owner: {owner}")

            print(f"Found recipient emails: {recipient_emails}")
            if recipient_emails:
                cc_emails = ['erdong.chen-ext@ldc.com']
                send_email(recipient_emails, cc_emails, story_data)
            else:
                print("No recipients found for the given owners.")

# run the main function every sleep_time seconds
while True:
    if config["control_flags"]["email"]:
        email()
    if config["control_flags"]["classify"]:
        classify()
    if config["control_flags"]["autoClose"]:
        autoClose()
    time.sleep(config['api']['sleep_time'])
