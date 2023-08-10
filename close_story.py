import requests
import json

# Load the cookies from the file
with open('cookies.json', 'r') as f:
    cookie_list = json.load(f)


def close_story(workspace_id, entity_id, cookie_list):
    # Set the URL
    url = f"https://www.tapd.cn/{workspace_id}/prong/stories/change_story_status/{entity_id}/storieslist/db"

    # Convert the list of cookie dictionaries to a string format
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookie_list])

    # Set up the headers
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookies,
        "Dsc-Token": "WKv2mCUaF9D784yf",
        "Host": "www.tapd.cn",
        "Origin": "https://www.tapd.cn",
        "Pragma": "no-cache",
        "Referer": f"https://www.tapd.cn/{workspace_id}/prong/stories/view/{entity_id}",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    # Set up the payload
    data = {
        "data[Story][current_status]": "status_7",
        "data[new_status]": "status_8",
        "data[editor]": "",
        "data[Comment][description]": ""
    }

    # Make the request
    response = requests.post(url, headers=headers, data=data, verify=False)
    
    # Check the response
    print(f"Response: {response.text}")

    return response.text

# Example usage:
close_story("55989309", "1155989309001001988",cookie_list)
