# data_utils.py

import requests
from datetime import datetime


# -------- Functions --------

# fetch a single data by entity_id
def fetch_data(workspace_id, entity_id, cookie_list):
    entity_id = "115598930900" + entity_id
    # Convert the list of cookie dictionaries to a string format
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookie_list])

    # Base URL
    base_url = f"https://www.tapd.cn/api/entity/comments/comment_list?workspace_id={workspace_id}&entity_id={entity_id}&page_size=10&page=1&entity_type=story&root_order_by=created+desc&reply_order_by=created+desc"

    # Parameters
    params = {
        'workspace_id': workspace_id,
        'entity_id': entity_id,
        'page_size': 10,
        'page': 1,
        'entity_type': 'story',
        'root_order_by': 'created+desc',
        'reply_order_by': 'created+desc'
    }

    # Headers
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': cookies,
        'Host': 'www.tapd.cn',
        'Referer': f'https://www.tapd.cn/{workspace_id}/prong/stories/view/{entity_id}?jump_count=1',
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # Make the request
    response = requests.get(base_url,  headers=headers, verify=False)

    # Parse the JSON response
    data = response.json()

    return data

# In most cases, earliest time would be the response time
def get_earliest_time(response_data):
    # Extract the 'comments' list from the data
    comments = response_data['data']['comments']

    # Check if the comments list is empty
    if not comments:
        return None

    # Extract the 'created' field from each comment and convert it to a datetime object
    created_times = [datetime.strptime(comment['created'], '%Y-%m-%d %H:%M:%S') for comment in comments]

    # Find the earliest time
    earliest_time = min(created_times)

    return earliest_time

# Define the function to fetch data and get the earliest time
def fetch_and_get_earliest_time(workspace_id, entity_id, cookie_list, fallback_date):
    # Fetch the data
    data = fetch_data(workspace_id, entity_id, cookie_list)

    # Get the earliest time
    try:
        earliest_time = get_earliest_time(data)
        if earliest_time is None:
            print(f"No comments found for entity_id {entity_id}. Using '完成时间' {fallback_date} instead.")
            if fallback_date == "":
                print(f"Error encountered when processing entity_id {entity_id}, no fallback date provided.")
                return None
            return fallback_date
    except ValueError:
        print(f"Error encountered when processing entity_id {entity_id}")
        return None

    print(f"The earliest time for entity_id {entity_id} is {earliest_time}")

    return earliest_time
