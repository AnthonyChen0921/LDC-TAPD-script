import requests
import json
from bs4 import BeautifulSoup
import re



def find_nearest_time(soup):
    # Searching for the given pattern in the table data elements
    td_elements = soup.find_all('td')
    for index, td in enumerate(td_elements):
        # First condition: "FN处理中" followed by "LDC确认中"
        if index + 1 < len(td_elements) and "FN处理中" in td.get_text() and "LDC确认中" in td_elements[index + 1].get_text():
            for prev_td in reversed(td_elements[:index]):
                if re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', prev_td.get_text()):
                    return prev_td.get_text()
            break

        # Second condition: "第三方处理中" followed by "LDC确认中"
        elif index + 1 < len(td_elements) and "第三方处理中" in td.get_text() and "LDC确认中" in td_elements[index + 1].get_text():
            for prev_td in reversed(td_elements[:index]):
                if re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', prev_td.get_text()):
                    return prev_td.get_text()
            break

    # If neither pattern is detected, search for the latest date right after <td>1</td>
    for index, td in enumerate(td_elements):
        if index + 1 < len(td_elements) and td.get_text().strip() == "1" and index + 1 < len(td_elements):
            next_td = td_elements[index + 1]
            if re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', next_td.get_text()):
                return next_td.get_text()
    return None


def getDate_FNToLDC(entity_id):
    # Load the cookies from the file
    with open('cookies.json', 'r') as f:
        cookie_list = json.load(f)

    # Convert the list of cookie dictionaries to a string format
        cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookie_list])

    # entity_id = "1001942"
    # Define headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Connection": "keep-alive",
        "Content-Encoding": "gzip",
        "Content-Type": "text/html; charset=UTF-8",
        "Cookie": cookies,
        "P3p": 'CP="NOI ADM DEV PSAi COM NAV OUR OTRo STP IND DEM"',
        "Tapd-Request-Name": "workitems::changes_list",
        "Tapd-Workspace-Id": "55989309",
        "X-Powered-By": "PHP/7.2.25",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Host": "www.tapd.cn",
        "Pragma": "no-cache",
        "Referer": f"https://www.tapd.cn/55989309/prong/stories/view/115598930900{entity_id}",
        "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    url = f"https://www.tapd.cn/55989309/prong/workitems/changes_list?perPage=10&workitem_type=story&workitem_id=115598930900{entity_id}&containerid=Revisions_div&tableclass=g_table&time=1691463553264"

    response = requests.get(url, headers=headers, verify=False)


    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        time_found = find_nearest_time(soup)
        
        if time_found:
            print(f"The Finished Time is found at {time_found}")
            return time_found
        else:
            print("No date found. Please Check manually.")
            return None

    else:
        print(f"Request failed with status code {response.status_code}")
        return None

def main():
    # Ask the user for the ID
    entity_id = input("Please enter the ID: ")

    # Get the date using the provided function
    date = getDate_FNToLDC(f"{entity_id}")

    # Print the result
    if date:
        print(f"Date found: {date}")
    else:
        print("No date found for the given ID.")

if __name__ == "__main__":
    main()


