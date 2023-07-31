import requests
import json
from datetime import datetime
import pandas as pd
import time

cookie_json_string = """
[
{
    "domain": ".tapd.cn",
    "expirationDate": 1722062525,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__root_domain_v",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": ".tapd.cn",
    "id": 1
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1722062529,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_qddaz",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "QD.780690508195708",
    "id": 2
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1691131360,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_t_crop",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "39151612",
    "id": 3
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1691131360,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_t_uid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "886333224",
    "id": 4
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1690531965.647047,
    "hostOnly": false,
    "httpOnly": true,
    "name": "_wt",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "eyJ1aWQiOiI4ODYzMzMyMjQiLCJjb21wYW55X2lkIjoiMzkxNTE2MTIiLCJleHAiOjE2OTA1MzE5NjV9.2c2c974d22cd3fe1e4dd67fa03244a7e77538e34d2012d10ccbb9fd2f65e197a",
    "id": 5
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1690612954,
    "hostOnly": false,
    "httpOnly": false,
    "name": "locale",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "zh_CN",
    "id": 6
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1691131359,
    "hostOnly": false,
    "httpOnly": true,
    "name": "t_u",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "46e611de59b96c28aac14b7a3ea32179caf52633a21345d5b05e9df4d630d5de39a873958281bd9f3a6b681baa93c51b5cf935a213dddc0774e0df8dca40b8765cc032474040c930%7C1",
    "id": 7
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1691131360,
    "hostOnly": false,
    "httpOnly": true,
    "name": "tapd_div",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "101_369",
    "id": 8
},
{
    "domain": ".tapd.cn",
    "expirationDate": 1691136475.661342,
    "hostOnly": false,
    "httpOnly": true,
    "name": "tapdsession",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1690526523163eb66a070f893076e2acf873a032cdabbc594cb25db86de82ffc7967749107",
    "id": 9
},
{
    "domain": "www.tapd.cn",
    "hostOnly": true,
    "httpOnly": false,
    "name": "_qddab",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "3-9102mn.lkm7ufda",
    "id": 10
},
{
    "domain": "www.tapd.cn",
    "hostOnly": true,
    "httpOnly": false,
    "name": "cloud_current_workspaceId",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "55989309",
    "id": 11
},
{
    "domain": "www.tapd.cn",
    "hostOnly": true,
    "httpOnly": false,
    "name": "dsc-token",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "uaCq59BE3oh3dcIk",
    "id": 12
}
]
"""

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
    response = requests.get(base_url,  headers=headers)

    # Parse the JSON response
    data = response.json()

    return data

# Your cookie data
cookie_list = json.loads(cookie_json_string)

# Your workspace_id and entity_id
workspace_id = '55989309'
# entity_id = '1155989309001001912'

# Fetch data
# data = fetch_data(workspace_id, entity_id, cookie_list)


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



########## read excel 

# Assuming your excel file is named 'input.xlsx' and is in the same directory as this script
df = pd.read_excel('input_small.xlsx')

# Define the function to fetch data and get the earliest time
def fetch_and_get_earliest_time(workspace_id, entity_id, cookie_list):
    # Fetch the data
    data = fetch_data(workspace_id, entity_id, cookie_list)

    # Get the earliest time
    try:
        earliest_time = get_earliest_time(data)
        if earliest_time is None:
            print(f"No comments found for entity_id {entity_id}")
            return None
    except ValueError:
        print(f"Error encountered when processing entity_id {entity_id}")
        return None

    print(f"The earliest time for entity_id {entity_id} is {earliest_time}")

    return earliest_time

# Iterate over each ID in the dataframe
for i, row in df.iterrows():
    entity_id = str(row['ID'])  # Assuming the column with the IDs is named 'ID'
    earliest_time = fetch_and_get_earliest_time(workspace_id, entity_id, cookie_list)

    # Add the earliest time to the '响应时间' column of the current row
    df.loc[i, '响应时间'] = earliest_time
    # Convert date to string
    earliest_time_str = earliest_time.strftime('%Y-%m-%d %H:%M:%S')
    df.loc[i, '响应时间_str'] = earliest_time_str

    # Print a success message
    print(f"{entity_id} completed, processing next request...")

    # Pause for a while to avoid hitting API rate limits
    time.sleep(0.5)  # sleep for 1.2 seconds

# Save the updated dataframe to a new excel file
df.to_excel('output.xlsx', index=False)


# if nothing goes wrong, should be succeed
print("success")




