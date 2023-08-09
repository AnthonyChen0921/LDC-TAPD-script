import time
import json
from fetch_story import fetch_story
from send_email import send_email

def load_email_map(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def update_contact_json(owner_name, path='contact.json'):
    """
    Update the contact.json file with a new owner and empty email.
    """
    with open(path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        # Add the new owner to the dictionary with an empty email
        data[owner_name] = ""
        # Reset the file position to the beginning
        f.seek(0)
        # Save the updated dictionary back to the file
        json.dump(data, f, ensure_ascii=False)
        # Truncate the file to remove any leftover content
        f.truncate()


def main():
    # load the previously fetched data
    try:
        with open('story.json', 'r') as file:
            old_data = json.load(file)
    except FileNotFoundError:
        old_data = {}


    # fetch the current data
    current_data_dict = fetch_story()

    # save the current data to a file for future comparison
    with open('story.json', 'w') as file:
        json.dump(current_data_dict, file)

    # check for changes in status from "status_3" to "status_7"
    for story_id, story_data in current_data_dict.items():
        old_story_data = old_data.get(story_id)
        if old_story_data is None:
            continue

        print(f'Checking story {story_id}...')
        if old_story_data['status'] == 'status_3' and story_data['status'] == 'status_7':
            # send email
            # Load email mapping
            email_map = load_email_map('contact.json')

            # Parse the owners and remove any empty strings after splitting
            owners = [owner.strip() for owner in story_data['owner'].split(';') if owner.strip()]
            print(f"Found owners: {owners}")

            recipient_emails = []
            for owner in owners:
                # find the recipient emails for each owner
                emails = email_map.get(owner)
                if emails:
                    # add email to the list
                    recipient_emails.append(emails)
                    print(f"Found recipients for owner: {owner}")
                else:
                    # If owner not found, update the contact.json with the owner's name in unicode
                    update_contact_json(owner)
                    print(f"⚠️ No recipients found for owner: {owner}. Added to contact.json")

            print(f"Found recipient emails: {recipient_emails}")
            # Ensure there are recipients to send the email to
            if recipient_emails:
                cc_emails = ['erdong.chen-ext@ldc.com'] # CC recipients
                send_email(recipient_emails, cc_emails, story_data)
            else:
                print("No recipients found for the given owners.")



# run the main function every 60 seconds
while True:
    main()
    time.sleep(10)
