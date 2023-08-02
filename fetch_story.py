import requests
import json

def fetch_story():
    url = "https://www.tapd.cn/api/aggregation/story_aggregation/get_story_fields_userviews_roles_workflowsteps_category_and_list"
    params = {
        "workspace_id": "55989309",
        "data[type]": "story",
        "location": "/prong/stories/stories_list",
        "data[query_token]": "f7404cf77c01fb0ca5a2d44f21f28fa8",
        "from": "stories_list"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "tapdsession=1690427294122b22268785cb4ba50ad2e7cba20166dcd118be8c5b1a4620834d0609d18857; come_from=https%3A%2F%2Fwww.google.com.hk%2F; __root_domain_v=.tapd.cn; _qddaz=QD.273690427302894; lastSE=google; app_locale_name=en; t_u=46e611de59b96c28aac14b7a3ea321799d0d7c78e387f9ea981ad252639995cf32a369b215e62cb4d2b7d280b4331960ca04483a12e2db0849ce9c31c54a5277782d71e3093b03c2%7C1; _t_uid=886333224; _t_crop=39151612; tapd_div=101_369; iteration_view_type_cookie=card_view; new_worktable=todo%7Cexpiration_date%7Cexpiration_date; cloud_current_workspaceId=55989309; dsc-token=1OaxKPDD0LFFc93M; _wt=eyJ1aWQiOiI4ODYzMzMyMjQiLCJjb21wYW55X2lkIjoiMzkxNTE2MTIiLCJleHAiOjE2OTA5NDA4Mjl9.94cf41e39ff8b61857c3174b3985d906a6ca23fe181e57ae4bc1b1ac5dab5008",
        "Host": "www.tapd.cn",
        "Origin": "https://www.tapd.cn",
        "Referer": "https://www.tapd.cn/tapd_fe/55989309/story/list?queryToken=f7404cf77c01fb0ca5a2d44f21f28fa8&categoryId=1155989309001000006&sort_name=&order=&useScene=storyList&conf_id=1155989309001004492&page=1",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    data = {"workspace_id":"55989309","conf_id":"1155989309001004492","sort_name":"","confIdType":"URL","order":"","perpage":"100","page":1,"query_token":"f7404cf77c01fb0ca5a2d44f21f28fa8","category_id":"0","location":"/prong/stories/stories_list","target":"55989309/story/list","entity_types":["story"],"use_scene":"storyList","list_type":"flat","need_category_counts":1,"menu_workitem_type_id":"","dsc_token":"1OaxKPDD0LFFc93M"}

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data), verify=False)

    # Parse the response JSON into a dictionary
    story_data = response.json()
    
    # Navigate to the list of stories
    stories = story_data['data']['stories_list']['data']['stories_list']

    # Form the dictionary using the list of stories
    story_data_dict = {story['Story']['id']: story['Story'] for story in stories}

    # Save the dictionary to a file
    with open('story.json', 'w') as file:
        json.dump(story_data_dict, file)

    print(f'Status Code: {response.status_code}')
    print('Story data has been fetched and saved to story.json')

    return story_data_dict
