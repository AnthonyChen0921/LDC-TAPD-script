import requests
import json

def download_and_save(session, url, filename):
    response = session.get(url)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)

def main():
    # Create a session
    session = requests.Session()

    # Set cookies
    cookies_json = """
    [
        {
            "name": "__root_domain_v",
            "value": ".tapd.cn"
        },
        {
            "name": "_qddaz",
            "value": "QD.780690508195708"
        },
        {
            "name": "_t_crop",
            "value": "39151612"
        },
        {
            "name": "_t_uid",
            "value": "886333224"
        },
        {
            "name": "locale",
            "value": "zh_CN"
        },
        {
            "name": "t_u",
            "value": "46e611de59b96c28aac14b7a3ea32179caf52633a21345d5b05e9df4d630d5de39a873958281bd9f3a6b681baa93c51b5cf935a213dddc0774e0df8dca40b8765cc032474040c930%7C1"
        },
        {
            "name": "tapd_div",
            "value": "101_369"
        },
        {
            "name": "tapdsession",
            "value": "169051028463035e8a075c95de87c657ce47ba2f12ff6fa87c543554eed09fdbb33efb03f2"
        },
        {
            "name": "_qdda",
            "value": "3-1.h3opx"
        },
        {
            "name": "_qddab",
            "value": "3-2k11s7.lkly6d2q"
        },
        {
            "name": "dsc-token",
            "value": "WKv2mCUaF9D784yf"
        }
    ]
    """

    # Load the JSON into a Python list
    cookies_list = json.loads(cookies_json)
    # Convert the list into a dictionary
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}
    
    session.cookies.update(cookies_dict)

    # Subpage URL
    subpage_url = 'https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.tapd.cn%2F55989309%2Fprong%2Fstories%2Fview%2F1155989309001001879%3Fjump_count%3D1&data=05%7C01%7Cchenerdong%40wustl.edu%7Cd4b0e84089c4464bbd0408db8f11fb12%7C4ccca3b571cd4e6d974b4d9beb96c6d6%7C0%7C0%7C638261079626824262%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=6ismX0%2F%2F3FJE8UzMe5hkNp%2BQ9FWot8d3LNbErB0OGAE%3D&reserved=0'  # replace with your actual subpage URL

    # Download and save the subpage
    filename = 'subpage.html'
    download_and_save(session, subpage_url, filename)

if __name__ == "__main__":
    main()
