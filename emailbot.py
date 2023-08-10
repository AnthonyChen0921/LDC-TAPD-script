import time
import json
from fetch_story import fetch_story
from send_email import send_email
from classify_story import classify_story
from fetch_story_unclassified import fetch_story_unclassified

# Load cookies from cookies.json
with open('cookies.json', 'r') as f:
    cookie_list = json.load(f)

def load_email_map(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def classify():
    # fetch unclassified data
    fetch_story_unclassified("55989309", cookie_list)

    # Load data from unclassified_story.json
    with open('story_unclassified.json', 'r') as f:
        stories_data = json.load(f)

    # Check each story
    for story_id, story_data in stories_data.items():
        story_name = story_data.get('name', '')
        if story_name.startswith("Case-"):
            workspace_id = story_data.get('workspace_id')
            print(f"not classified {story_id} and {story_data}")
            classify_story(workspace_id, story_id, cookie_list)
    


def email():
    # load the previously fetched data
    try:
        with open('story.json', 'r') as file:
            old_data = json.load(file)
    except FileNotFoundError:
        old_data = {}


    # fetch the current data
    current_data_dict = fetch_story("55989309", cookie_list)

    # save the current data to a file for future comparison
    with open('story.json', 'w') as file:
        json.dump(current_data_dict, file)

    # check for changes in status from "status_3" to "status_7"
    for story_id, story_data in current_data_dict.items():
        old_story_data = old_data.get(story_id)
        if old_story_data is None:
            continue

        if old_story_data['status'] == 'status_3' and story_data['status'] == 'status_7':
            # send email
            # Load email mapping
            email_map = load_email_map('contact.json')  # replace with the correct path to your JSON file

            # Parse the owners and remove any empty strings after splitting
            owners = [owner.strip() for owner in story_data['owner'].split(';') if owner.strip()]
            print(f"Found owners: {owners}")

            recipient_emails = []
            for owner in owners:
                # find the recipient emails for each owner
                emails = email_map.get(owner)
                if emails:
                    # add email to ths list
                    recipient_emails.append(emails)
                    print(f"Found recipients for owner: {owner}")
                else:
                    # print unicode char for owner
                    print(f"⚠️ No recipients found for owner: {owner}")

            print(f"Found recipient emails: {recipient_emails}")
            # Ensure there are recipients to send the email to
            if recipient_emails != []:
                cc_emails = ['erdong.chen-ext@ldc.com'] # CC recipients
                send_email(recipient_emails, cc_emails, story_data)
            else:
                print("No recipients found for the given owners.")


# run the main function every 60 seconds
while True:
    email()
    classify()
    time.sleep(10)
