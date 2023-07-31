import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = 'https://www.tapd.cn/55989309/prong/stories/view/1155989309001001870'

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

# response = requests.get(url, cookies=cookies)

# Now `response` should be the same as if you had loaded the page in your browser while logged in
print(response.text)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <span> tags with the specific class attribute
span_tags = soup.find_all('span', attrs={'class': 'field-time'})

# Extract the text from the span tags
timestamps = [tag.text for tag in span_tags]

# Print the timestamps
for timestamp in timestamps:
    print(timestamp)

# To get the earliest timestamp, you may need to convert the timestamps to datetime objects.
# Here is a basic example of how you can do that, but you may need to adjust the format depending on how the timestamps are formatted on your website.

from datetime import datetime

# Convert the timestamps to datetime objects
datetimes = [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") for timestamp in timestamps]

# Get the earliest datetime
earliest = min(datetimes)

print("Earliest:", earliest)