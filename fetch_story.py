import requests
import json

# Load the cookies from the file
with open('cookies.json', 'r') as f:
    cookie_list = json.load(f)

def fetch_story(workspace_id, cookie_list, page):
    # Convert the list of cookie dictionaries to a string format
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookie_list])

    url = "https://www.tapd.cn/api/aggregation/story_aggregation/get_story_fields_userviews_roles_workflowsteps_category_and_list"
    params = {
        "workspace_id": workspace_id,
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
        "Cookie": cookies,
        "Host": "www.tapd.cn",
        "Origin": "https://www.tapd.cn",
        "Referer": f"https://www.tapd.cn/tapd_fe/{workspace_id}/story/list?queryToken=f7404cf77c01fb0ca5a2d44f21f28fa8&categoryId=1155989309001000006&sort_name=&order=&useScene=storyList&conf_id=1155989309001004492&page=1",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    data = {
        "workspace_id": workspace_id,
        "conf_id": "1155989309001004492",
        "sort_name": "",
        "confIdType": "URL",
        "order": "",
        "perpage": 100,
        "page": page,
        "query_token": "d4b7ab949c883a3890cff3254503140d",
        "category_id": "1155989309001000006",
        "location": "/prong/stories/stories_list",
        "useScene": "storyList",
        "entity_types": ["story"],
        "list_type": "tree",
        "need_category_counts": 1,
        "menu_workitem_type_id": "",
        "dsc_token": "WKv2mCUaF9D784yf",
        "exclude_workspace_configs": [],
        "filter_data": {},
        "selected_workspace_ids": []
    }


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
