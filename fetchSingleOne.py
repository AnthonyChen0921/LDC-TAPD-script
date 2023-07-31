import requests
import json

# Your URL
url = "https://www.tapd.cn/api/entity/comments/comment_list?workspace_id=55989309&entity_id=1155989309001001870&page_size=10&page=1&entity_type=story&root_order_by=created+desc&reply_order_by=created+desc"

# Your headers
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': '__root_domain_v=.tapd.cn; _qddaz=QD.780690508195708; _t_crop=39151612; _t_uid=886333224; locale=zh_CN; t_u=46e611de59b96c28aac14b7a3ea32179caf52633a21345d5b05e9df4d630d5de39a873958281bd9f3a6b681baa93c51b5cf935a213dddc0774e0df8dca40b8765cc032474040c930%7C1; tapd_div=101_369; tapdsession=1690526523163eb66a070f893076e2acf873a032cdabbc594cb25db86de82ffc7967749107; _qddab=3-9102mn.lkm7ufda; _wt=eyJ1aWQiOiI4ODYzMzMyMjQiLCJjb21wYW55X2lkIjoiMzkxNTE2MTIiLCJleHAiOjE2OTA1MzA3NDB9.a6ba2090a97f06d521015c60ea060b2c6507023f99772da486ecda8aa937cac9',
    'Host': 'www.tapd.cn',
    'Referer': 'https://www.tapd.cn/55989309/prong/stories/view/1155989309001001870?jump_count=1',
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
response = requests.get(url, headers=headers)

# Parse the JSON response
data = response.json()

# Print the data
print(json.dumps(data, indent=4))
