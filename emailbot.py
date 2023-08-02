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
            # trim last 7 char of story_id
            story_id_short = story_id[:-7]
            # prepare email content
            subject = f'【ID{story_id_short}】{story_data["name"]}待确认'
            # 如果对处理结果不满意的，请将“处理人”还原为上一位富农产品/开发/测试的名字，并将状态更新为“FN处理中”。
            body = f'【ID{story_id_short} ({story_data["name"]}, created by {story_data["creator"]}) has changed its status from "status_3" to "status_7".'

            # send email
            send_email('erdong.chen-ext@ldc.com', subject, body)
        else:
            print(f'Story {story_id} has not changed status.')

# run the main function every 60 seconds
while True:
    main()
    time.sleep(10)
