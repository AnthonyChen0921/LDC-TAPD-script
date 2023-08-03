import time
import json
from fetch_story import fetch_story
from send_email import send_email

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
            # send email
            to_emails = ['erdong.chen-ext@ldc.com', 'chenerdong0921@gmail.com'] # recipients
            cc_emails = ['erdong.chen-ext@ldc.com'] # CC recipients

            send_email(to_emails, cc_emails, story_data)
    
            print(f'Story {story_id} changed status, email already sent.')
        else:
            print(f'Story {story_id} has not changed status.')

# run the main function every 60 seconds
while True:
    main()
    time.sleep(10)
