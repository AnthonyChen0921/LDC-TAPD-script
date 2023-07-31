import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = 'https://www.tapd.cn/tapd_fe/55989309/story/list?categoryId=1155989309001000006&sort_name=&order=&useScene=storyList&conf_id=1155989309001004492&page=1'

# Your cookie data
cookies = {
    "__root_domain_v": ".tapd.cn",
    "_qddaz": "QD.780690508195708",
    "_t_crop": "39151612",
    "_t_uid": "886333224",
    "_wt": "eyJ1aWQiOiI4ODYzMzMyMjQiLCJjb21wYW55X2lkIjoiMzkxNTE2MTIiLCJleHAiOjE2OTA1MjY4NjB9.e6f6293a1a6bff8c6cef9a5b971577bc36e20a5555c42505771657029c534008",
    "locale": "zh_CN",
    "t_u": "46e611de59b96c28aac14b7a3ea32179caf52633a21345d5b05e9df4d630d5de39a873958281bd9f3a6b681baa93c51b5cf935a213dddc0774e0df8dca40b8765cc032474040c930%7C1",
    "tapd_div": "101_369",
    "tapdsession": "1690526523163eb66a070f893076e2acf873a032cdabbc594cb25db86de82ffc7967749107",
    "_qdda": "3-1.3b9to7",
    "_qddab": "3-9102mn.lkm7ufda",
    "sso-login-token": "605578938e6d13ee5c52275439ee7f10"
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, cookies=cookies, headers=headers)

# print first line of response
print(response.text)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <a> tags with the specific data attribute
a_tags = soup.find_all('a', attrs={'data-v-4ed37476': ''})

# Extract the href attributes
urls = [tag.get('href') for tag in a_tags]

# Print the href attributes of the matching <a> tags
for url in urls:
    print(url)
